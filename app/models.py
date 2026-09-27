# -*- coding:utf-8 -*-
import hashlib
from datetime import datetime

from flask import current_app
from flask_login import AnonymousUserMixin, UserMixin
from itsdangerous import URLSafeTimedSerializer as Serializer
from werkzeug.security import check_password_hash, generate_password_hash

from . import db, login_manager


class Permission:
    FOLLOW = 1
    COMMENT = 2
    WRITE = 4
    MODERATE = 8
    ADMINISTER = 16


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64), unique=True, index=True)
    username = db.Column(db.String(64), unique=True)
    password_hash = db.Column(db.String(128))
    confirmed = db.Column(db.Boolean, default=None)
    name = db.Column(db.String(64))
    location = db.Column(db.TEXT)
    about_me = db.Column(db.TEXT)
    member_since = db.Column(db.DateTime(), default=datetime.utcnow)
    last_seen = db.Column(db.DateTime(), default=datetime.utcnow)
    avatar_hash = db.Column(db.String(32))
    column1 = db.Column(db.String(64))
    column2 = db.Column(db.String(64))
    column3 = db.Column(db.String(64))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()

    class AnonymousUser(AnonymousUserMixin):
        def can(self, permissions):
            return False

        def is_administrator(self):
            return False

    def ping(self):
        self.last_seen = datetime.utcnow()
        db.session.add(self)
        try:
            db.session.commit()
        except Exception:
            db.session.rollback()

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'confirm': self.id})

    def confirm(self, token, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=expiration)
        except Exception:
            return False
        if self.id == data.get('confirm'):
            self.confirmed = True
            db.session.add(self)
            db.session.commit()
            return True
        return False

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=expiration)
        except Exception:
            return False
        if self.id == data.get('reset'):
            self.password = new_password
            db.session.add(self)
            db.session.commit()
            return True
        return False

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token, max_age=expiration)
        except Exception:
            return False
        if data.get('new_email') is None:
            return False
        if self.id == data.get('change_email'):
            self.email = data.get('new_email')
            self.avatar_hash = hashlib.md5(
                self.email.encode('utf-8')).hexdigest()
            db.session.add(self)
            db.session.commit()
            return True
        return False

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)

    @staticmethod
    def generate_fake(count=100):
        from random import seed, choice
        import string
        from sqlalchemy.exc import IntegrityError

        try:
            import forgery_py
            has_forgery = True
        except ImportError:
            has_forgery = False

        seed()
        for i in range(count):
            if has_forgery:
                u = User(email=forgery_py.internet.email_address(),
                         username=forgery_py.internet.user_name(True) + str(i),
                         password=forgery_py.lorem_ipsum.word(),
                         confirmed=True,
                         name=forgery_py.name.full_name(),
                         location=forgery_py.address.city(),
                         about_me=forgery_py.lorem_ipsum.sentence(),
                         member_since=forgery_py.date.date(True)
                         )
            else:
                rand_str = ''.join(choice(string.ascii_lowercase)
                                   for _ in range(6))
                u = User(email=f'user{i}_{rand_str}@example.com',
                         username=f'user{i}_{rand_str}',
                         password='password123',
                         confirmed=True,
                         name=f'User {i}',
                         location='City',
                         about_me='Just a test user.')
            db.session.add(u)
            try:
                db.session.commit()
            except IntegrityError:
                db.session.rollback()

    def __repr__(self):
        return '<User %r>' % self.name


class Post(db.Model):
    __tablename__ = 'posts'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(255), unique=True)
    abstract = db.Column(db.Text)
    content = db.Column(db.Text)
    url = db.Column(db.String(255), unique=True)
    image = db.Column(db.Text)
    web_site = db.Column(db.String(64))
    category = db.Column(db.String(64))
    others = db.Column(db.Text)
    publish_time = db.Column(db.DateTime)
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def generate_fake(count=100):
        from random import randint, seed, choice

        try:
            import forgery_py
            has_forgery = True
        except ImportError:
            has_forgery = False

        seed()
        categories = ['Technology', 'Sports', 'Money', 'Hot', 'Entertainment']
        for i in range(count):
            cat = choice(categories)
            if has_forgery:
                p = Post(title=forgery_py.lorem_ipsum.sentences(randint(1, 3)) + f' {i}',
                         content=forgery_py.lorem_ipsum.sentences(
                             randint(1, 3)),
                         abstract=forgery_py.lorem_ipsum.sentences(1),
                         url=f'http://example.com/post/{i}',
                         category=cat,
                         web_site='Example News',
                         publish_time=datetime.utcnow())
            else:
                p = Post(title=f'Sample Article Title {i}',
                         content=f'Sample content for article {i}.',
                         abstract=f'Sample abstract for article {i}.',
                         url=f'http://example.com/post/{i}',
                         category=cat,
                         web_site='Example News',
                         publish_time=datetime.utcnow())
            db.session.add(p)
            try:
                db.session.commit()
            except Exception:
                db.session.rollback()


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    create_time = db.Column(db.DateTime, index=True, default=datetime.utcnow)

    @staticmethod
    def insert_categories():
        categories = ['Technology', 'Sports', 'Money', 'Hot', 'Entertainment']
        for name in categories:
            category = Category.query.filter_by(name=name).first()
            if category is None:
                category = Category(name=name)
            category.name = name
            db.session.add(category)
        db.session.commit()

    def __repr__(self):
        return '<Category %r>' % self.name
