# -*- coding: utf-8 -*-#
# --------------------------------------------------------------------------
# ProjectName：albumy
# Name:models.py
# Description: 数据库模型
# Author:ChenQiancheng
# Date:2023/11/1  23:31
# --------------------------------------------------------------------------
from datetime import datetime
from flask import current_app
from flask_login import UserMixin
from albumy.extensions import db
from werkzeug.security import generate_password_hash, check_password_hash

# relationship table
roles_permissions = db.Table('roles_permissions',
                             db.Column('role_id', db.Integer, db.ForeignKey('role.id')),
                             db.Column('permission_id', db.Integer, db.ForeignKey('permission.id'))
                             )


class Permission(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    roles = db.relationship('Role', secondary=roles_permissions, back_populates='permissions')


class Role(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), unique=True)
    users = db.relationship('User', back_populates='role')
    permissions = db.relationship('Permission', secondary=roles_permissions, back_populates='roles')

    @staticmethod
    def init_role():
        roles_permissions_map = {
            'Locked': ['FOLLOW', 'COLLECT'],
            'User': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD'],
            'Moderator': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD', 'MODERATE'],
            'Administrator': ['FOLLOW', 'COLLECT', 'COMMENT', 'UPLOAD', 'MODERATE', 'ADMINISTER']
        }

        for role_name in roles_permissions_map:
            role = Role.query.filter_by(name=role_name).first()
            if role is None:
                role = Role(name=role_name)
                db.session.add(role)
            role.permissions = []
            for permission_name in roles_permissions_map[role_name]:
                permission = Permission.query.filter_by(name=permission_name).first()
                if permission is None:
                    permission = Permission(name=permission_name)
                    db.session.add(permission)
                role.permissions.append(permission)
        db.session.commit()


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

    role_id = db.Column(db.Integer, db.ForeignKey('role.id'))

    role = db.relationship('Role', back_populates='users')

    def __init__(self, **kwargs):
        super(User, self).__init__(**kwargs)
        self.generate_avatar()
        self.follow(self)  # follow self
        self.set_role()

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def set_role(self):
        if self.role is None:
            if self.email == current_app.config['ALBUMY_ADMIN_EMAIL']:
                self.role = Role.query.filter_by(name='Administrator').first()
            else:
                self.role = Role.query.filter_by(name='User').first()
            db.session.commit()

    def validate_password(self, password):
        return check_password_hash(self.password_hash, password)

    # def follow(self, user):
    #     if not self.is_following(user):
    #         follow = Follow(follower=self, followed=user)
    #         db.session.add(follow)
    #         db.session.commit()
    #
    # def unfollow(self, user):
    #     follow = self.following.filter_by(followed_id=user.id).first()
    #     if follow:
    #         db.session.delete(follow)
    #         db.session.commit()
    #
    # def is_following(self, user):
    #     if user.id is None:  # when follow self, user.id will be None
    #         return False
    #     return self.following.filter_by(followed_id=user.id).first() is not None
    #
    # def is_followed_by(self, user):
    #     return self.followers.filter_by(follower_id=user.id).first() is not None
    #
    # @property
    # def followed_photos(self):
    #     return Photo.query.join(Follow, Follow.followed_id == Photo.author_id).filter(Follow.follower_id == self.id)
    #
    # def collect(self, photo):
    #     if not self.is_collecting(photo):
    #         collect = Collect(collector=self, collected=photo)
    #         db.session.add(collect)
    #         db.session.commit()
    #
    # def uncollect(self, photo):
    #     collect = Collect.query.with_parent(self).filter_by(collected_id=photo.id).first()
    #     if collect:
    #         db.session.delete(collect)
    #         db.session.commit()
    #
    # def is_collecting(self, photo):
    #     return Collect.query.with_parent(self).filter_by(collected_id=photo.id).first() is not None
    #
    # def lock(self):
    #     self.locked = True
    #     self.role = Role.query.filter_by(name='Locked').first()
    #     db.session.commit()
    #
    # def unlock(self):
    #     self.locked = False
    #     self.role = Role.query.filter_by(name='User').first()
    #     db.session.commit()
    #
    # def block(self):
    #     self.active = False
    #     db.session.commit()
    #
    # def unblock(self):
    #     self.active = True
    #     db.session.commit()
    #
    # def generate_avatar(self):
    #     avatar = Identicon()
    #     filenames = avatar.generate(text=self.username)
    #     self.avatar_s = filenames[0]
    #     self.avatar_m = filenames[1]
    #     self.avatar_l = filenames[2]
    #     db.session.commit()

    @property
    def is_admin(self):
        return self.role.name == 'Administrator'

    # @property
    # def is_active(self):
    #     return self.active

    def can(self, permission_name):
        permission = Permission.query.filter_by(name=permission_name).first()
        return permission is not None and self.role is not None and permission in self.role.permissions
