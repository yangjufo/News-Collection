# News-Collection

## Basic information

A website collects and shows news from the Internet, based on Flask.

Deployed on AWS, address: https://news.jianyang995.com/

## Support
1. Categoried news
2. User management (register, log in, password/email update, email verification, etc.)
3. Column customization
4. Atuo updatied news (everyday)

## Requirements
1. MySQL
2. Python 3.6.x

## How to run
### Configuration
Change configuration in ```app/config.py```
1. Change email setting: my_email, MAIL_USERNAME, MAIL_SERVER, MAIL_PASSWORD => It is similar with using a third party  mail client to control your mailbox and then send emails.
2. Change databse setting: db_cfg (user, passwd) => If you want to use Chinese in database, you need to change the character set of MySQL to utf8.

### Start server
1. Install requirements: ```pip install -r requests.txt```
2. Create table in database: run ```python manage.py deploy``` in root directory
3. Collect news from Internet: run ```python toutiao.py&``` in directory ```spider```
4. Run the server: run ```python manage.py runserver``` in root directory
5. Open link http://127.0.0.1:5000/

## Demo
### Homepage
![alt homepage](https://raw.githubusercontent.com/yangjufo/News-Collection/master/readme/homepage.png)
### Log in
![alt homepage](https://raw.githubusercontent.com/yangjufo/News-Collection/master/readme/login.png)




