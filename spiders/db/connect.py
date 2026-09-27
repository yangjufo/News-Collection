# -*- coding: utf-8 -*-

# Define here the models

import os
import socket
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

basedir = os.path.abspath(os.path.dirname(__file__))
project_root = os.path.abspath(os.path.join(basedir, '..', '..'))

db_cfg = {
    'host': os.environ.get('MYSQL_HOST', '127.0.0.1'),
    'port': int(os.environ.get('MYSQL_PORT', 3306)),
    'user': os.environ.get('MYSQL_USER', 'root'),
    'passwd': os.environ.get('MYSQL_PASSWORD', '12138'),
    'db': os.environ.get('MYSQL_DB', 'newsCollection'),
    'encoding': 'utf-8'
}


def _normalize_sqlite_uri(uri):
    if uri and uri.startswith('sqlite:///'):
        path = uri[len('sqlite:///'):]
        if path == ':memory:':
            return uri
        if not path.startswith('/'):
            abs_path = os.path.abspath(os.path.join(project_root, path))
            return f'sqlite:///{abs_path}'
    return uri


def _get_engine():
    if os.environ.get('DATABASE_URL'):
        return create_engine(_normalize_sqlite_uri(os.environ['DATABASE_URL']))
    if os.environ.get('SQLALCHEMY_DATABASE_URI'):
        return create_engine(_normalize_sqlite_uri(os.environ['SQLALCHEMY_DATABASE_URI']))

    host = db_cfg['host']
    port = db_cfg['port']
    has_mysql_env = bool(os.environ.get('MYSQL_HOST')
                         or os.environ.get('MYSQL_DB'))

    if not has_mysql_env:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.settimeout(0.2)
                if s.connect_ex((host, port)) != 0:
                    sqlite_path = os.path.join(project_root, 'data.sqlite')
                    return create_engine(f'sqlite:///{sqlite_path}')
        except Exception:
            sqlite_path = os.path.join(project_root, 'data.sqlite')
            return create_engine(f'sqlite:///{sqlite_path}')

    return create_engine('mysql+pymysql://{user}:{passwd}@{host}:{port}/{db}?charset=utf8&use_unicode=1'.format(**db_cfg))


test_engine = _get_engine()
TestDBSession = sessionmaker(bind=test_engine)
