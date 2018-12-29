# -*- coding: utf-8 -*-

import json
import time
import traceback

from db.connect import test_engine, TestDBSession
from db.models import Article
from tools import *

test_conn = test_engine.connect()
session = TestDBSession()


def toutiao_spider(category_web, category_db):
    start_url = 'http://www.toutiao.com/api/pc/feed/'
    time_stamp = time.time()
    param = {
        "category": category_web,
        "utm_source": "toutiao",
        "widen": "1",
        "max_behot_time": str(time_stamp),
        "max_behot_time_tmp": str(time_stamp),
        "tadrequire": "true",
        "as": "A1053924239A06B",
        "cp": "5943CAE086FBEE1"
    }
    count = 0
    for i in range(0, 100):
        param['max_behot_time'] = param['max_behot_time_tmp'] = str(time_stamp - i * 20 * 60)
        response = get_page(url=start_url, params=param)
        json_obj = json.loads(response)
        if count >= 200:
            break
        for one in json_obj.get('data'):
            if not one:
                continue
            count += 1
            source_url = 'http://www.toutiao.com' + one.get('source_url', '')
            title = one.get('title', '')
            behot_time = one.get('behot_time', '')
            x = time.localtime(behot_time)
            behot_time = time.strftime('%Y-%m-%d %H:%M:%S', x)
            abstract = one.get('abstract', '')
            image_url = one.get('image_url', '')
            category = category_db
            web_site = '今日头条'
            article = Article(url=source_url, title=title, publish_time=behot_time, abstract=abstract, image=image_url,
                              category=category, web_site=web_site)
            print(title)
            if article and image_url:
                session.add(article)
                try:
                    session.commit()
                except:
                    print(traceback.print_exc())
                    session.rollback()


def main():
    while True:
        toutiao_spider("news_hot", "Hot")
        toutiao_spider("news_finance", "Money")
        toutiao_spider("news_entertainment", "Entertainment")
        toutiao_spider("news_tech", "Technology")
        toutiao_spider("news_sports", "Sports")
        time.sleep(86400)


if __name__ == '__main__':
    main()
