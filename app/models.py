# -*- coding:utf-8 -*-
import hashlib
from datetime import datetime

from flask import current_app
from flask_login import UserMixin, AnonymousUserMixin
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from werkzeug.security import generate_password_hash, check_password_hash

from . import db
from . import login_manager


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
    member_since = db.Column(db.DateTime(), default=datetime.now())
    last_seen = db.Column(db.DateTime(), default=datetime.now())
    avatar_hash = db.Column(db.String(32))
    column1 = db.Column(db.String(64), )
    column2 = db.Column(db.String(64))
    column3 = db.Column(db.String(64))

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        if self.email is not None and self.avatar_hash is None:
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8')).hexdigest()

    class AnonymousUser(AnonymousUserMixin):
        def can(self, permissions):
            return False

        def is_administrator(self):
            return False

    def ping(self):
        self.last_seen = datetime.now()
        db.session.add(self)

    def generate_confirmation_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'confirm': self.id})

    def confirm(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if self.id == data.get('confirm'):
            self.confirmed = True
            db.session.add(self)
            return True
        return False

    def generate_reset_token(self, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'reset': self.id})

    def reset_password(self, token, new_password):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if self.id == data.get('reset'):
            self.password = new_password
            db.session.add(self)
            return True
        return False

    def generate_email_change_token(self, new_email, expiration=3600):
        s = Serializer(current_app.config['SECRET_KEY'], expiration)
        return s.dumps({'change_email': self.id, 'new_email': new_email})

    def change_email(self, token):
        s = Serializer(current_app.config['SECRET_KEY'])
        try:
            data = s.loads(token)
        except:
            return False
        if data.get('new_email') is None:
            return False
        if self.id == data.get('change_email'):
            self.email = data.get('new_email')
            self.avatar_hash = hashlib.md5(self.email.encode('utf-8').hexdigest())
            db.session.add(self)
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
        from sqlalchemy.exc import IntegrityError
        from random import seed
        import forgery_py

        seed()
        for i in range(count):
            u = User(email=forgery_py.internet.email_address(),
                     username=forgery_py.internet.user_name(True),
                     password=forgery_py.lorem_ipsum.word(),
                     confirmed=True,
                     name=forgery_py.name.full_name(),
                     location=forgery_py.address.city(),
                     about_me=forgery_py.lorem_ipsum.sentence(),
                     member_since=forgery_py.date.date(True)
                     )
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
    create_time = db.Column(db.DateTime, index=True, default=datetime.now())

    @staticmethod
    def generate_fake(count=100):
        from random import seed, randint
        import forgery_py

        seed()
        user_count = User.query.count()
        for i in range(count):
            p = Post(title=forgery_py.lorem_ipsum.sentences(randint(1, 3)),
                     content=forgery_py.lorem_ipsum.sentences(randint(1, 3)), create_time=forgery_py.date.date(True))
            db.session.add(p)
            db.session.commit()


class Category(db.Model):
    __tablename__ = 'categories'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(64))
    create_time = db.Column(db.DateTime, index=True, default=datetime.now())

    @staticmethod
    def insert_categories():
        categories = ['Technology', 'Sports', 'Money', 'Hot', 'Entertainment']
        for name in categories:
            category = Category.query.filter_by(name=name).first()
            if category is None:
                category = Category(name=category)
            category.name = name
            db.session.add(category)
        db.session.commit()

    def __repr__(self):
        return '<Category %r>' % self.name
