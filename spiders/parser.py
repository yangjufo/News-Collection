# -*- coding: utf-8 -*-
"""
Robust XML RSS 2.0 and Atom 1.0 feed parser for News-Collection.
Parses articles, extracts summaries, images, dates, and cleans HTML formatting.
"""

import re
import html
import xml.etree.ElementTree as ET
from datetime import datetime
from email.utils import parsedate_to_datetime

try:
    from .feeds import CATEGORY_PLACEHOLDER_IMAGES
except (ImportError, ValueError):
    from feeds import CATEGORY_PLACEHOLDER_IMAGES

MEDIA_NS = '{http://search.yahoo.com/mrss/}'
ATOM_NS = '{http://www.w3.org/2005/Atom}'


def clean_html(raw_html):
    """Strip HTML tags and unescape HTML entities."""
    if not raw_html:
        return ''
    # Remove script and style elements
    text = re.sub(r'<(script|style)[^>]*>.*?</\1>',
                  '', raw_html, flags=re.DOTALL | re.IGNORECASE)
    # Strip HTML tags
    text = re.sub(r'<[^>]+>', ' ', text)
    # Unescape HTML entities
    text = html.unescape(text)
    text = html.unescape(text)
    # Replace non-breaking spaces
    text = text.replace('\xa0', ' ')
    # Normalize multiple whitespace characters
    text = re.sub(r'\s+', ' ', text).strip()
    return text


def parse_datetime(date_str):
    """Parse RFC 2822 or ISO 8601 date string to naive UTC datetime."""
    if not date_str:
        return datetime.utcnow()

    date_str = date_str.strip()

    # Try RFC 2822 (common in RSS 2.0)
    try:
        dt = parsedate_to_datetime(date_str)
        if dt.tzinfo is not None:
            # Convert to naive UTC
            dt = dt.astimezone().replace(tzinfo=None)
        return dt
    except Exception:
        pass

    # Try ISO 8601 (common in Atom 1.0)
    try:
        clean_iso = date_str.replace('Z', '+00:00')
        dt = datetime.fromisoformat(clean_iso)
        if dt.tzinfo is not None:
            dt = dt.astimezone().replace(tzinfo=None)
        return dt
    except Exception:
        pass

    # Try standard string formats
    formats = [
        '%Y-%m-%d %H:%M:%S',
        '%Y-%m-%dT%H:%M:%S',
        '%Y-%m-%d',
    ]
    for fmt in formats:
        try:
            return datetime.strptime(date_str, fmt)
        except Exception:
            continue

    return datetime.utcnow()


def extract_image_url(element, raw_text=''):
    """Extract an image URL from media tags, enclosure tags, or description HTML."""
    # 1. Check enclosure tag
    enclosure = element.find('enclosure')
    if enclosure is not None:
        url = enclosure.attrib.get('url', '')
        enc_type = enclosure.attrib.get('type', '')
        if url and ('image' in enc_type or url.lower().endswith(('.jpg', '.jpeg', '.png', '.webp', '.gif'))):
            return url

    # 2. Check media:content or media:thumbnail
    for tag in ['content', 'thumbnail']:
        for media_elem in element.findall(f'{MEDIA_NS}{tag}'):
            url = media_elem.attrib.get('url', '')
            if url:
                return url

    # 3. Check for <img> tags inside description or content
    if raw_text:
        match = re.search(
            r'<img[^>]+src=["\']([^"\']+)["\']', raw_text, re.IGNORECASE)
        if match:
            candidate = match.group(1).strip()
            if candidate.startswith(('http://', 'https://')):
                return candidate

    return None


def parse_feed_content(xml_text, default_category='Technology', default_source='News'):
    """
    Parses RSS 2.0 or Atom 1.0 XML content and returns a list of article dictionaries.
    """
    articles = []
    if not xml_text:
        return articles

    try:
        # Handle string or bytes
        if isinstance(xml_text, str):
            xml_bytes = xml_text.encode('utf-8', errors='replace')
        else:
            xml_bytes = xml_text

        root = ET.fromstring(xml_bytes)
    except Exception:
        return articles

    fallback_img = CATEGORY_PLACEHOLDER_IMAGES.get(
        default_category, CATEGORY_PLACEHOLDER_IMAGES['Technology'])

    # Determine if RSS or Atom
    tag_name = root.tag.lower()

    if 'feed' in tag_name:
        # Atom 1.0 feed
        entries = root.findall(
            f'.//{ATOM_NS}entry') or root.findall('.//entry')
        for entry in entries:
            title_elem = entry.find(f'{ATOM_NS}title') or entry.find('title')
            title = clean_html(
                title_elem.text if title_elem is not None else '')
            if not title:
                continue

            # Link
            link = ''
            links = entry.findall(f'{ATOM_NS}link') or entry.findall('link')
            for l in links:
                rel = l.attrib.get('rel', 'alternate')
                if rel in ('alternate', ''):
                    link = l.attrib.get('href', '')
                    if link:
                        break
            if not link and links:
                link = links[0].attrib.get('href', '')
            if not link:
                continue

            # Summary / Content
            summary_elem = entry.find(
                f'{ATOM_NS}summary') or entry.find('summary')
            content_elem = entry.find(
                f'{ATOM_NS}content') or entry.find('content')
            raw_summary = summary_elem.text if summary_elem is not None else (
                content_elem.text if content_elem is not None else '')
            clean_summary = clean_html(raw_summary)

            # Date
            updated_elem = entry.find(f'{ATOM_NS}updated') or entry.find(
                'updated') or entry.find(f'{ATOM_NS}published') or entry.find('published')
            date_str = updated_elem.text if updated_elem is not None else ''
            publish_time = parse_datetime(date_str)

            # Image
            img_url = extract_image_url(entry, raw_summary) or fallback_img

            articles.append({
                'title': title[:250],
                'url': link[:250],
                'abstract': clean_summary[:500] if clean_summary else title,
                'content': clean_summary,
                'image': img_url,
                'web_site': default_source[:64],
                'category': default_category[:64],
                'publish_time': publish_time
            })

    else:
        # RSS 2.0 feed
        items = root.findall('.//item')
        for item in items:
            title_elem = item.find('title')
            title = clean_html(
                title_elem.text if title_elem is not None else '')
            if not title:
                continue

            link_elem = item.find('link')
            link = (link_elem.text if link_elem is not None else '').strip()
            if not link:
                continue

            desc_elem = item.find('description')
            raw_desc = desc_elem.text if desc_elem is not None else ''
            clean_desc = clean_html(raw_desc)

            pub_date_elem = item.find('pubDate')
            date_str = pub_date_elem.text if pub_date_elem is not None else ''
            publish_time = parse_datetime(date_str)

            img_url = extract_image_url(item, raw_desc) or fallback_img

            articles.append({
                'title': title[:250],
                'url': link[:250],
                'abstract': clean_desc[:500] if clean_desc else title,
                'content': clean_desc,
                'image': img_url,
                'web_site': default_source[:64],
                'category': default_category[:64],
                'publish_time': publish_time
            })

    return articles
