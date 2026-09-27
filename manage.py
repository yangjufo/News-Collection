#!/usr/bin/env python

import os
import sys
import click

from app import create_app, db
from app.models import User, Post, Category
from flask_migrate import Migrate
from flask.cli import FlaskGroup

application = create_app(os.getenv('FLASK_CONFIG') or 'default')
migrate = Migrate(application, db)


@application.shell_context_processor
def make_shell_context():
    return dict(app=application, db=db, User=User, Post=Post, Category=Category)


@application.cli.command('deploy')
def deploy():
    """Deploy and initialize database tables and seed categories."""
    with application.app_context():
        db.drop_all()
        db.create_all()
        Category.insert_categories()
    print("Database tables created and categories seeded.")


def find_available_port(host, preferred_port):
    import socket
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, preferred_port))
            return preferred_port
    except Exception:
        pass
    for p in [5001, 5050, 8000, 8080]:
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind((host, p))
                print(
                    f" * Port {preferred_port} is in use. Automatically switched to port {p}.")
                return p
        except Exception:
            continue
    return preferred_port


@application.cli.command('runserver')
@click.option('--host', '-h', default='0.0.0.0', help='The interface to bind to.')
@click.option('--port', '-p', default=5000, type=int, help='The port to bind to.')
@click.option('--debug/--no-debug', default=True, help='Enable or disable debug mode.')
def runserver(host, port, debug):
    """Run the Flask development server."""
    from werkzeug.serving import run_simple
    actual_port = find_available_port(host, port)
    run_simple(host, actual_port, application,
               use_reloader=debug, use_debugger=debug)


@application.cli.command('test')
def test():
    """Run the unit tests."""
    import unittest
    tests = unittest.TestLoader().discover('tests')
    result = unittest.TextTestRunner(verbosity=2).run(tests)
    if not result.wasSuccessful():
        sys.exit(1)


@application.cli.command('crawl')
@click.option('--category', '-c', default='all', help='Category to crawl (Technology, Sports, Money, Hot, Entertainment, or all).')
@click.option('--limit', '-l', default=15, type=int, help='Maximum articles per feed.')
@click.option('--clear/--no-clear', default=False, help='Clear existing articles before crawling.')
@click.option('--mock/--no-mock', default=False, help='Generate sample articles directly without network.')
def crawl(category, limit, clear, mock):
    """Crawl and update news articles from RSS and news feeds."""
    spider_dir = os.path.join(os.path.dirname(
        os.path.abspath(__file__)), 'spiders')
    if spider_dir not in sys.path:
        sys.path.insert(0, spider_dir)
    from news_spider import crawl_all
    crawl_all(category=category, limit_per_feed=limit,
              clear_first=clear, mock=mock)


cli = FlaskGroup(create_app=lambda: application)

if __name__ == "__main__":
    if len(sys.argv) == 1:
        from werkzeug.serving import run_simple
        actual_port = find_available_port('0.0.0.0', 5000)
        run_simple('0.0.0.0', actual_port, application,
                   use_reloader=True, use_debugger=True)
    else:
        cli()
