# -*- coding: utf-8 -*-#
# --------------------------------------------------------------------------
# ProjectName：albumy
# Name:models.py
# Description: 数据库模型
# Author:ChenQiancheng
# Date:2023/11/1  23:31
# --------------------------------------------------------------------------
from datetime import datetime
from flask_login import UserMixin
from albumy.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    # 资料
    username = db.Column(db.String(20), unique=True, index=True)
    email = db.Column(db.String(254), unique=True, index=True)
    password_hash = db.Column(db.String(128))
    name = db.Column(db.String(30))
    website = db.Column(db.String(255))
    bio = db.Column(db.String(120))
    location = db.Column(db.String(50))
    member_since = db.Column(db.DateTime, default=datetime.utcnow)
    # 用户状态
    confirmed = db.Column(db.Boolean, default=False)

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)