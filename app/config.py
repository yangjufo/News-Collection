# -*- coding:utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))
my_email = '156416776@qq.com'  # change to your own email
SECRET_KEY = 'hard to guess string.'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

FLASKY_POSTS_PER_PAGE = 10
FLASKY_MAIL_SUBJECT_PREFIX = '[News Collection - Your Channel]'
FLASKY_MAIL_SENDER = my_email
FLASKY_ADMIN = my_email
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = '156416776@qq.com'

DEBUG = True

MAIL_PASSWORD = ''

db_cfg={
    'host': '127.0.0.1',
    'port':3306,
    'user': 'root',
    'passwd': '',
    'db': 'newsCollection',
    'encoding':'utf-8'
}

SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}?charset=utf8&use_unicode=1'.format(**db_cfg)
