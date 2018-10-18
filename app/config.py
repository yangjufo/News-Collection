# -*- coding:utf-8 -*-
import os

basedir = os.path.abspath(os.path.dirname(__file__))
my_email = '156416776@qq.com'  # 换成自己qq邮箱
SECRET_KEY = 'hard to guss string.'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = True

FLASKY_POSTS_PER_PAGE = 20
FLASKY_MAIL_SUBJECT_PREFIX = '[新闻聚合-你的专属新闻站]'
FLASKY_MAIL_SENDER = my_email
FLASKY_ADMIN = my_email
MAIL_SERVER = 'smtp.qq.com'
MAIL_PORT = 465
MAIL_USE_SSL = True
MAIL_USERNAME = '156416776@qq.com'

DEBUG = True

MAIL_PASSWORD = 'utzibwltpohxbibe'  # 邮箱授权码
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root@127.0.0.1/pyblog'
