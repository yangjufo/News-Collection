# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField

from ..models import Category


class EditProfileForm(FlaskForm):
    def __init__(self, *args, **kwargs):
        super(EditProfileForm, self).__init__(*args, **kwargs)
        self.choices = [(cate.name, cate.name) if cate else '' for cate in Category.query.all()]
        self.column1.choices = self.choices
        self.column2.choices = self.choices
        self.column3.choices = self.choices

    column1 = SelectField('栏目一')
    column2 = SelectField('栏目二')
    column3 = SelectField('栏目三')
    submit = SubmitField('提交')
