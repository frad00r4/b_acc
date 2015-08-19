# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask import render_template
from . import business_accounting


@business_accounting.route('costs', defaults={'page': 1})
@business_accounting.route('costs/<int:page>')
def costs(page):
    return render_template('b_acc/costs.html')
