#!/bin/sh

source_folder=/home/ubuntu/sites/news.jianyang995.com

cd $source_folder/News-Collection/spiders/
$source_folder/env/bin/python toutiao_spider.py

