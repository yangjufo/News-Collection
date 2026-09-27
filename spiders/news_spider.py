# -*- coding: utf-8 -*-
"""
Main News Spider for News-Collection.
Aggregates news from Chinese and English RSS/Atom feeds across 5 categories:
Technology, Sports, Money, Hot, Entertainment.
Features automatic deduplication, image extraction, and offline fallback.
"""

from parser import parse_feed_content
from feeds import FEED_SOURCES, get_mock_articles
from db.models import Article
from db.connect import test_engine, TestDBSession
import requests
import sys
import os
import argparse
import logging
from datetime import datetime

# Ensure project and spider directories are on sys.path
current_dir = os.path.dirname(os.path.abspath(__file__))
project_root = os.path.dirname(current_dir)
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if project_root not in sys.path:
    sys.path.insert(0, project_root)


logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    datefmt='%H:%M:%S'
)
logger = logging.getLogger('news_spider')

HEADERS = {
    'User-Agent': (
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64) '
        'AppleWebKit/537.36 (KHTML, like Gecko) '
        'Chrome/120.0.0.0 Safari/537.36'
    ),
    'Accept': 'application/rss+xml, application/atom+xml, application/xml, text/xml, */*',
    'Accept-Language': 'zh-CN,zh;q=0.9,en-US;q=0.8,en;q=0.7',
}


def fetch_feed_data(url, timeout=8):
    """Fetch raw XML data from a feed URL."""
    try:
        response = requests.get(url, headers=HEADERS, timeout=timeout)
        if response.status_code == 200:
            return response.content
        logger.warning(f'HTTP {response.status_code} when fetching {url}')
        return None
    except requests.exceptions.Timeout:
        logger.warning(f'Timeout fetching {url}')
        return None
    except requests.exceptions.RequestException as e:
        logger.warning(f'Failed to fetch {url}: {e}')
        return None


def save_articles(session, article_dicts, limit=20):
    """
    Saves a list of article dictionaries to the database.
    Skips duplicates based on URL or Title.
    Returns the count of newly saved articles.
    """
    saved_count = 0
    for data in article_dicts[:limit]:
        title = data.get('title', '').strip()
        url = data.get('url', '').strip()
        if not title or not url:
            continue

        # Check for duplicates
        existing = session.query(Article).filter(
            (Article.url == url) | (Article.title == title)
        ).first()

        if existing:
            continue

        article = Article(
            url=url,
            title=title,
            abstract=data.get('abstract', '')[:1000],
            content=data.get('content', ''),
            image=data.get('image', ''),
            web_site=data.get('web_site', 'Internet')[:64],
            category=data.get('category', 'Hot')[:64],
            publish_time=data.get('publish_time', datetime.utcnow())
        )
        session.add(article)
        try:
            session.commit()
            saved_count += 1
        except Exception as e:
            session.rollback()

    return saved_count


def crawl_category(session, category, limit_per_feed=15, timeout=8):
    """Crawl all feed sources for a given category."""
    sources = FEED_SOURCES.get(category, [])
    category_saved = 0
    successful_feeds = 0

    for source in sources:
        name = source['name']
        url = source['url']
        logger.info(f'Fetching [{category}] {name} ({source["lang"]})...')

        xml_data = fetch_feed_data(url, timeout=timeout)
        if not xml_data:
            continue

        articles = parse_feed_content(
            xml_data, default_category=category, default_source=name)
        if articles:
            newly_saved = save_articles(
                session, articles, limit=limit_per_feed)
            logger.info(
                f'  -> {name}: {len(articles)} parsed, {newly_saved} new saved.')
            category_saved += newly_saved
            successful_feeds += 1
        else:
            logger.warning(f'  -> {name}: 0 articles parsed.')

    return category_saved, successful_feeds


def crawl_all(category=None, limit_per_feed=15, timeout=8, clear_first=False, mock=False):
    """
    Main crawling coordinator.
    """
    session = TestDBSession()
    total_saved = 0

    if clear_first:
        logger.info('Clearing old articles from database...')
        try:
            if category and category.lower() != 'all':
                session.query(Article).filter_by(category=category).delete()
            else:
                session.query(Article).delete()
            session.commit()
            logger.info('Old articles cleared.')
        except Exception as e:
            session.rollback()
            logger.error(f'Error clearing old articles: {e}')

    target_categories = [category] if (category and category.lower(
    ) != 'all' and category in FEED_SOURCES) else list(FEED_SOURCES.keys())

    if mock:
        logger.info(
            'Running in Mock Mode (generating bilingual sample articles)...')
        for cat in target_categories:
            mock_items = get_mock_articles(category=cat, count=limit_per_feed)
            saved = save_articles(session, mock_items, limit=limit_per_feed)
            total_saved += saved
            logger.info(
                f'[{cat}] Generated {len(mock_items)} mock articles, {saved} new saved.')
        session.close()
        return total_saved

    total_successful_feeds = 0
    for cat in target_categories:
        saved, succ_feeds = crawl_category(
            session, cat, limit_per_feed=limit_per_feed, timeout=timeout)
        total_saved += saved
        total_successful_feeds += succ_feeds

    # If no feeds succeeded (e.g. offline/isolated environment), use fallback mock articles
    if total_successful_feeds == 0:
        logger.warning(
            'All network feeds were unreachable (offline or restricted network).')
        logger.info('Falling back to high-quality bilingual sample news...')
        for cat in target_categories:
            mock_items = get_mock_articles(category=cat, count=limit_per_feed)
            saved = save_articles(session, mock_items, limit=limit_per_feed)
            total_saved += saved
            logger.info(
                f'[{cat}] Fallback generated {len(mock_items)} items, {saved} new saved.')

    session.close()
    logger.info(f'Finished crawling! Total new articles added: {total_saved}')
    return total_saved


def main():
    parser = argparse.ArgumentParser(
        description='News-Collection Multi-Source RSS & News Spider')
    parser.add_argument('--category', '-c', default='all',
                        help='Category to crawl (Technology, Sports, Money, Hot, Entertainment, or all)')
    parser.add_argument('--limit', '-l', type=int, default=15,
                        help='Maximum articles to save per feed')
    parser.add_argument('--timeout', '-t', type=int, default=8,
                        help='HTTP request timeout in seconds')
    parser.add_argument('--clear', action='store_true',
                        help='Clear existing articles before crawling')
    parser.add_argument('--mock', action='store_true',
                        help='Generate mock bilingual news without network access')

    args = parser.parse_args()
    crawl_all(
        category=args.category,
        limit_per_feed=args.limit,
        timeout=args.timeout,
        clear_first=args.clear,
        mock=args.mock
    )


if __name__ == '__main__':
    main()
