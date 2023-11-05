# -*- coding: utf-8 -*-#
# --------------------------------------------------------------------------
# ProjectName：albumy
# Name:decorators.py
# Description:  装饰器
# Author:ChenQiancheng
# Date:2023/11/1  23:30
# --------------------------------------------------------------------------
from functools import wraps
from flask import Markup, flash, url_for, redirect
from flask_login import current_user


# 过滤未确认用户
def confirm_required(func):
    @wraps(func)
    def decorated_function(*args, **kwargs):
        if not current_user.confirm:
            message = Markup(
                'Please confirm your account first.'
                'Not receive the email?'
                '<a class="alert-link" href="%s">Resend Confirm Email</a>' %
                url_for('auth.resend_confirm_email'))
            flash(message, 'warning')
            return redirect(url_for('main.index'))
        return func(*args, **kwargs)
    return decorated_function
