#!/bin/bash

source_folder=/home/ubuntu/sites/news.jianyang995.com

sudo service nginx reload
$source_folder/env/bin/gunicorn --bind unix:/tmp/news.jianyang995.com.socket wsgi:application&
