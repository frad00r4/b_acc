# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask import render_template
from . import business_accounting


@business_accounting.route('price', defaults={'page': 1})
@business_accounting.route('price/<int:page>')
def price(page):
    return render_template('b_acc/price.html')
