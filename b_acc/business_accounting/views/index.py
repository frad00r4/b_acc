# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask import render_template
from ...exts import connection
from . import business_accounting


@business_accounting.route('/')
def index():
    money = None
    return render_template('b_acc/index.html', money=money)
