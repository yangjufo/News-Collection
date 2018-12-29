# -*- coding:utf-8 -*-
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, PasswordField, BooleanField, ValidationError
from wtforms.validators import DataRequired, Length, Email, Regexp, EqualTo
from ..models import User


class LoginForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    remember_me = BooleanField('Keep me logged in')
    submit = SubmitField('Log in')


class RegistrationForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    username = StringField('Username', validators=[DataRequired(), Length(1, 64), Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0,
                                                                                         'Username must start with a '
                                                                                         'letter and can only contain: '
                                                                                         'letters, numbers, dots, '
                                                                                         'and underscores')])
    password = PasswordField('Password', validators=[DataRequired(), Length(6, 64, message='Password must have at '
                                                                                           'least 6 letters')])
    password2 = PasswordField('Confirm password',
                              validators=[DataRequired(), EqualTo('password', message='Password must match.')])
    submit = SubmitField('Register')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first():
            raise ValidationError('Email is registered!')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username exists!')


class ChangePasswordForm(FlaskForm):
    old_password = PasswordField('Password', validators=[DataRequired()])
    password = PasswordField('New password', validators=[DataRequired()])
    password2 = PasswordField('Confirm password',
                              validators=[DataRequired(), EqualTo('password', message='Passwords must match!')])
    submit = SubmitField('Submit', validators=[DataRequired()])


class PasswordResetForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('New password', validators=[DataRequired()])
    password2 = PasswordField('Confirm password',
                              validators=[DataRequired(), EqualTo('password', message='Passwords must match.')])
    submit = SubmitField('Submit')

    def validate_email(self, field):
        if User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Email is not registered!')


class PasswordResetRequestForm(FlaskForm):
    email = StringField('Email', validators=[DataRequired(), Length(1, 64), Email()])
    submit = SubmitField('Submit')


class EmailResetForm(FlaskForm):
    email = StringField('New email', validators=[DataRequired(), Length(1, 64), Email()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Submit')

    @staticmethod
    def validate_email(field):
        if not User.query.filter_by(email=field.data).first() is None:
            raise ValidationError('Email is registered!')
