# -*- coding:utf-8 -*-
from flask import render_template, redirect, request, url_for, flash
from flask_login import login_user, login_required, logout_user, current_user
from . import auth
from ..models import User
from .. import db
from .forms import LoginForm, RegistrationForm, ChangePasswordForm, PasswordResetForm, PasswordResetRequestForm, \
    EmailResetForm
from ..email import send_email


@auth.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is not None and user.verify_password(form.password.data):
            login_user(user, form.remember_me.data)
            return redirect(request.args.get('next') or url_for('main.index'))
        flash('Invalid username or password!')
    return render_template('auth/login.html', form=form)


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have logged out!')
    return redirect(url_for('main.index'))


@auth.route('/register', methods=['GET', 'POST'])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(email=form.email.data, username=form.username.data, password=form.password.data)
        db.session.add(user)
        db.session.commit()
        token = user.generate_confirmation_token()
        send_email(user.email, 'Verification', 'auth/email/confirm', user=user, token=token)
        flash('Verification mail has sent to you mailbox!')
        return redirect(url_for('main.index'))
    return render_template('auth/register.html', form=form)


@auth.route('/confirm')
def resend_confirmation():
    token = current_user.generate_confirmation_token()
    send_email(current_user.email, 'Verification', 'auth/email/confirm', user=current_user, token=token)
    flash('Verification mail has sent to you mailbox!')
    return redirect(url_for('main.index'))


@auth.route('/confirm/<token>')
@login_required
def confirm(token):
    if current_user.confirmed:
        return redirect(url_for('main.index'))
    if current_user.confirm(token):
        flash('Verification succeeds!')
    else:
        flash('Verification link is invalid!')
    return redirect(url_for('main.index'))


@auth.before_app_request
def before_request():
    if current_user.is_authenticated:
        current_user.ping()
        if not current_user.confirmed and request.endpoint[:5] != 'auth.' and request.endpoint != 'static':
            return redirect(url_for('auth.unconfirmed'))


@auth.route('/unconfirmed')
def unconfirmed():
    if current_user.is_anonymous or current_user.confirmed:
        redirect(url_for('main.index'))
    return render_template('auth/unconfirmed.html')


@auth.route('/auth.immediate_confirm')
def immediate_confirm():
    current_user.confirmed = True
    db.session.add(current_user)
    return redirect(url_for('auth.login'))


@auth.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.old_password.data):
            current_user.password = form.password.data
            db.session.add(current_user)
            flash('Password reset succeeds!')
            return redirect(url_for('main.index'))
        else:
            flash('Password is incorrect!')
    return render_template('auth/change_password.html', form=form)


@auth.route('/reset', methods=['GET', 'POST'])
def password_reset_request():
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetRequestForm()
    user = User.query.filter_by(email=form.email.data).first()
    if user:
        token = user.generate_reset_token()
        send_email(user.email, 'Password Reset', 'auth/email/reset_password', user=user, token=token)
        flash('Password reset mail has sent to you mailbox!')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/reset/<token>', methods=['GET', 'POST'])
def password_reset(token):
    if not current_user.is_anonymous:
        return redirect(url_for('main.index'))
    form = PasswordResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user is None:
            return redirect(url_for('main.index'))
        if user.reset_password(token, form.password.data):
            flash('Password reset succeeds!')
            return redirect(url_for('auth.login'))
        return redirect(url_for('main.index'))
    return render_template('auth/reset_password.html', form=form)


@auth.route('/change_email', methods=['GET', 'POST'])
@login_required
def change_email_request():
    form = EmailResetForm()
    if form.validate_on_submit():
        if current_user.verify_password(form.password.data):
            new_email = form.email.data
            token = current_user.generate_email_change_token(new_email)
            send_email(new_email, 'Confirm Email', 'auth/email/change_email', user=current_user, token=token)
            flash('Confirm mail has sent to your mailbox!')
            return redirect(url_for('main.index'))
        else:
            flash('Password is incorrect!')
    return render_template('auth/change_email.html', form=form)


@auth.route('/change_email/<token>', methods=['GET', 'POST'])
@login_required
def change_email(token):
    if current_user.change_email(token):
        flash('Email change succeeds!')
    else:
        flash('Email hange link is invalid!')
    return redirect(url_for('main.index'))

