# -*- coding: utf-8 -*-#
# --------------------------------------------------------------------------
# ProjectName：albumy
# Name:auth.py
# Description:
# Author:ChenQiancheng
# Date:2023/11/1  23:27
# --------------------------------------------------------------------------
from albumy.forms.auth import RegisterForm
from albumy.models import User
from albumy.settings import Operations
from albumy.emails import send_confirm_email
from flask import Blueprint, redirect, url_for, flash, render_template
from flask_login import current_user
from albumy.extensions import db
from albumy.utils import generate_token

auth_bp = Blueprint('auth', __name__)


@auth_bp.route('register', methods=['GET', 'POST'])
def register():
    # 判断用户是否通过认证
    if current_user.is_authenticated:
        return redirect(url_for('main.index'))
    form = RegisterForm()
    if form.validate_on_submit():
        name = form.name.data
        email = form.email.data.lower()
        username = form.username.data
        password = form.password.data
        user = User(name=name, email=email, username=username)
        # 设置密码
        user.set_password(password)
        db.session.add(user)
        db.session.commit()
        token = generate_token(user=name, operation=Operations.CONFIRM)
        send_confirm_email(user=user, token=token)
        flash('Confirm email sent, check your inbox.', 'info')
        return redirect(url_for('.login'))
    return render_template('auth/register.html', form=form)
