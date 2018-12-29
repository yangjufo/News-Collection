# -*- coding:utf-8 -*-
import jieba
from flask import render_template, redirect, url_for, flash, request
from flask_login import current_user, login_required

from . import main
from .forms import EditProfileForm
from .. import db
from ..models import Post, Category


@main.route('/', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    cur_category = request.args.get('category', '')
    query_set = Post.query
    if cur_category:
        query_set = query_set.filter_by(category=cur_category)
    pagination = query_set.order_by(Post.publish_time.desc(), Post.id.desc()).paginate(page, per_page=50,
                                                                                       error_out=False)
    articles = pagination.items
    print(articles)
    sub_cates = []
    if current_user.is_authenticated:
        sub_cates = [current_user.column1, current_user.column2, current_user.column3]
    columns = list(set([cate.name.strip() for cate in Category.query.all()]) - set(sub_cates))
    categories = filter(lambda x: True if isinstance(x, str) and len(x) >= 2 else False, (sub_cates + columns)[:10])
    return render_template('index.html', articles=articles, pagination=pagination,
                           categories=categories, cur_category=cur_category)


@main.route('/subscribe/', methods=['GET', 'POST'])
@login_required
def subscribe():
    form = EditProfileForm()
    if form.validate_on_submit():
        current_user.column1 = form.column1.data.strip()
        current_user.column2 = form.column2.data.strip()
        current_user.column3 = form.column3.data.strip()
        db.session.add(current_user)
        flash('Subscription has updated!')
        return redirect(url_for('.subscribe'))
    form.column1.data = current_user.column1
    form.column2.data = current_user.column2
    form.column3.data = current_user.column3

    sub_cates = []
    if current_user.is_authenticated:
        sub_cates = [current_user.column1, current_user.column2, current_user.column3]
    columns = list(set([cate.name.strip() for cate in Category.query.all()]) - set(sub_cates))
    categories = filter(lambda x: True if isinstance(x, str) and len(x) >= 2 else False, (sub_cates + columns)[:10])
    return render_template('/subscribe.html', form=form, categories=categories)


@main.route('/information')
@login_required
def information():
    return render_template('/user.html')
