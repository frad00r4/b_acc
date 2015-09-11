# -*- coding: utf-8 -*-

from flask import render_template
from . import business_accounting


__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'


@business_accounting.route('/')
def index():
    money = None
    return render_template('b_acc/index.html', money=money)
