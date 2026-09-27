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
1. Python 3.6+ / 3.10+
2. MySQL (optional: automatically falls back to SQLite for local development)

## How to run
### Configuration
Change configuration in ```app/config.py``` or set environment variables (`DATABASE_URL`, `MYSQL_HOST`, etc.):
1. Change email setting: my_email, MAIL_USERNAME, MAIL_SERVER, MAIL_PASSWORD => It is similar to using a third party mail client to control your mailbox and send emails.
2. Change database setting: `DATABASE_URL` or `db_cfg` (user, passwd). If MySQL is not running locally, SQLite (`data.sqlite`) is automatically used.

### Start server
1. Install requirements: ```pip install -r requirements.txt```
2. Create table in database: run ```python manage.py deploy``` in root directory
3. Collect news:
   - From project root: ```python manage.py crawl```
   - Or from directory ```spiders```: ```python news_spider.py``` (or ```./repeat.sh```)
   - Useful options: ```--category Technology```, ```--limit 10```, ```--clear```, ```--mock``` (offline mode)
4. Run the server: run ```python manage.py runserver``` or ```python wsgi.py```
5. Open link http://127.0.0.1:5000/

## Demo
### Homepage
![alt homepage](https://raw.githubusercontent.com/yangjufo/News-Collection/master/readme/homepage.png)
### Log in
![alt login page](https://raw.githubusercontent.com/yangjufo/News-Collection/master/readme/login.png)
