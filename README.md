Website collects and shows news from the Internet, based on Flask.

## 配置
数据库使用mysql
语言是python 3.6.x
在models文件中修改数据库用户名密码

## 运行
1. pip install -r requests.txt 安装依赖包
2. 根目录下python manage.py deploy创建数据库表
3. 运行spiders文件夹下的toutiao_spider.py和netease_spider
4. 根目录下运行python manage.py runserver
5. 在127.0.0.1:5000查看结果


