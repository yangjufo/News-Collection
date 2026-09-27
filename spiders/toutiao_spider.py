# -*- coding: utf-8 -*-
"""
Legacy entry point for news spider.
Delegates to the modern multi-source news_spider.
"""

from news_spider import crawl_all
import sys
import os

current_dir = os.path.dirname(os.path.abspath(__file__))
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)


def main():
    crawl_all(limit_per_feed=15, timeout=8)


if __name__ == '__main__':
    main()
