# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from sqlalchemy import Column, Integer, DateTime, String, VARCHAR, TEXT
from sqlalchemy.ext.declarative import declarative_base

from .connect import test_engine

# 创建对象的基类:
Base = declarative_base()

from datetime import datetime


class Article(Base):
    # table name:
    __tablename__ = 'posts'

    # table columns:
    id = Column(Integer(), primary_key=True)
    url = Column(VARCHAR(255), unique=True)
    title = Column(VARCHAR(255), unique=True)
    abstract = Column(TEXT)
    content = Column(TEXT)
    image = Column(TEXT)
    web_site = Column(String(64))
    category = Column(String(64))
    others = Column(TEXT)
    publish_time = Column(DateTime)
    create_time = Column(DateTime, index=True, default=datetime.now())


Base.metadata.create_all(test_engine)  # 创建表
