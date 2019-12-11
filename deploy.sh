#!/bin/bash

source_folder=/home/ubuntu/sites/news.jianyang995.com
cd $source_folder/News-Collection
git pull

sed -i 's/DEBUG = True/DEBUG = False/' ./app/config.py 

sudo service nginx reload
$source_folder/env/bin/gunicorn --bind unix:/tmp/news.jianyang995.com.socket wsgi:application&
