import os
import sys
import unittest

from app import create_app, db
from app.models import Post
from spiders.feeds import get_mock_articles
from spiders.parser import parse_feed_content, clean_html, parse_datetime


class SpiderTestCase(unittest.TestCase):
    def setUp(self):
        self.app = create_app('testing')
        self.app_context = self.app.app_context()
        self.app_context.push()
        db.create_all()

    def tearDown(self):
        db.session.remove()
        db.drop_all()
        self.app_context.pop()

    def test_clean_html(self):
        raw = '<p>Hello <b>World</b>&amp;nbsp;!</p>'
        self.assertEqual(clean_html(raw), 'Hello World !')

    def test_parse_datetime(self):
        rfc_date = 'Mon, 22 Sep 2026 14:30:00 +0000'
        dt = parse_datetime(rfc_date)
        self.assertEqual(dt.year, 2026)
        self.assertEqual(dt.month, 9)
        self.assertEqual(dt.day, 22)

    def test_parse_rss_feed(self):
        sample_rss = """<?xml version="1.0" encoding="UTF-8"?>
        <rss version="2.0">
          <channel>
            <title>Tech Feed</title>
            <item>
              <title>New Supercomputer Announced</title>
              <link>https://example.com/supercomputer</link>
              <description>&lt;p&gt;Breakthrough processing speeds achieved.&lt;/p&gt;</description>
              <pubDate>Mon, 22 Sep 2026 10:00:00 +0000</pubDate>
            </item>
          </channel>
        </rss>"""
        articles = parse_feed_content(
            sample_rss, default_category='Technology', default_source='TechSource')
        self.assertEqual(len(articles), 1)
        self.assertEqual(articles[0]['title'], 'New Supercomputer Announced')
        self.assertEqual(articles[0]['category'], 'Technology')
        self.assertEqual(articles[0]['web_site'], 'TechSource')
        self.assertTrue(articles[0]['image'].startswith('http'))

    def test_mock_articles_generation(self):
        items = get_mock_articles(category='Technology', count=5)
        self.assertTrue(len(items) > 0)
        self.assertEqual(items[0]['category'], 'Technology')
        self.assertTrue(bool(items[0]['title']))
        self.assertTrue(bool(items[0]['image']))

    def test_save_parsed_articles(self):
        items = get_mock_articles(category='Technology', count=3)
        for item in items:
            p = Post(
                url=item['url'],
                title=item['title'],
                abstract=item['abstract'],
                content=item['content'],
                image=item['image'],
                web_site=item['web_site'],
                category=item['category'],
                publish_time=item['publish_time']
            )
            db.session.add(p)
        db.session.commit()
        self.assertEqual(Post.query.count(), 3)
