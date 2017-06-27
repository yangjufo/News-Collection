# -*- coding:utf-8-*-
from selenium import webdriver
import time
import re
import datetime
import traceback
import random
from spiders.db.connect import test_engine, TestDBSession
from spiders.db.models import Article

test_conn = test_engine.connect()
session = TestDBSession()
day = datetime.datetime.now()
driver = webdriver.PhantomJS(executable_path="phantomjs.exe")


def netease_spider(start_url, category, web_site):
    driver.get(start_url)
    time.sleep(3)
    for link in driver.find_elements_by_class_name("na_pic"):
        print(link.get_attribute("href"))
        if re.match("^" + start_url + "/17/0" + str(day.month) + str(day.day),
                    str(link.get_attribute("href"))) or re.match(
                                            "^" + start_url + "/17/0" + str(day.month) + str(day.day - 1),
            str(link.get_attribute("href"))):
            source_url = link.get_attribute('href')
            img = link.find_element_by_tag_name("img")
            title = img.get_attribute("alt")
            image_url = img.get_attribute("src")
            x = time.time() - random.randint(300, 30000)
            x = time.localtime(x)
            behot_time = time.strftime('%Y-%m-%d %H:%M:%S', x)
            category = category
            web_site = web_site
            print(title)
            article = Article(url=source_url, title=title, publish_time=behot_time, image=image_url,
                              category=category, web_site=web_site)
            if article and image_url:
                session.add(article)
                try:
                    session.commit()
                except:
                    print(traceback.print_exc())
                    session.rollback()


def main():
    while True:
        netease_spider("http://tech.163.com", "科技", "网易科技")
        netease_spider("http://sports.163.com", "体育", "网易体育")
        time.sleep(86400)


if __name__ == '__main__':
    main()
