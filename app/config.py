# -*- coding:utf-8 -*-
import os
import socket

basedir = os.path.abspath(os.path.dirname(__file__))
my_email = '156416776@qq.com'  # change to your own email
SECRET_KEY = os.environ.get('SECRET_KEY') or 'hard to guess string.'
SQLALCHEMY_COMMIT_ON_TEARDOWN = True
SQLALCHEMY_TRACK_MODIFICATIONS = False

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

db_cfg = {
    'host': os.environ.get('MYSQL_HOST', '127.0.0.1'),
    'port': int(os.environ.get('MYSQL_PORT', 3306)),
    'user': os.environ.get('MYSQL_USER', 'root'),
    'passwd': os.environ.get('MYSQL_PASSWORD', ''),
    'db': os.environ.get('MYSQL_DB', 'newsCollection'),
    'encoding': 'utf-8'
}


def _normalize_sqlite_uri(uri):
    if uri and uri.startswith('sqlite:///'):
        path = uri[len('sqlite:///'):]
        if path == ':memory:':
            return uri
        if not path.startswith('/'):
            abs_path = os.path.abspath(
                os.path.join(os.path.dirname(basedir), path))
            return f'sqlite:///{abs_path}'
    return uri


def _get_database_uri():
    if os.environ.get('DATABASE_URL'):
        return _normalize_sqlite_uri(os.environ.get('DATABASE_URL'))
    if os.environ.get('SQLALCHEMY_DATABASE_URI'):
        return _normalize_sqlite_uri(os.environ.get('SQLALCHEMY_DATABASE_URI'))

    # If explicit MySQL environment variable was provided, or if local MySQL port is open
    host = db_cfg['host']
    port = db_cfg['port']
    has_mysql_env = bool(os.environ.get('MYSQL_HOST')
                         or os.environ.get('MYSQL_DB'))

    if not has_mysql_env:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.2)
                if s.connect_ex((host, port)) != 0:
                    sqlite_path = os.path.join(
                        os.path.dirname(basedir), 'data.sqlite')
                    return f'sqlite:///{sqlite_path}'
        except Exception:
            sqlite_path = os.path.join(os.path.dirname(basedir), 'data.sqlite')
            return f'sqlite:///{sqlite_path}'

    return 'mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}?charset=utf8&use_unicode=1'.format(**db_cfg)


SQLALCHEMY_DATABASE_URI = _get_database_uri()
