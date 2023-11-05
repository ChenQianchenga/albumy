# -*- coding: utf-8 -*-#
# --------------------------------------------------------------------------
# ProjectName：albumy
# Name:main.py
# Description:
# Author:ChenQiancheng
# Date:2023/11/1  23:27
# --------------------------------------------------------------------------
import os

from flask import render_template, flash, redirect, url_for, current_app, \
    send_from_directory, request, abort, Blueprint
from flask_login import login_required, current_user
from albumy.utils import rename_image, resize_image, redirect_back, flash_errors

main_bp = Blueprint('main', __name__)


@main_bp.route('/')
def index():
    return "hello world"


@main_bp.route('/explore')
def explore():
    # photos = Photo.query.order_by(func.random()).limit(12)
    # return render_template('main/explore.html', photos=photos)
    return "explore"
