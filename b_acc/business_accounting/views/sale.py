# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask import render_template
from ..models import Goods
from . import business_accounting


@business_accounting.route('sales')
def sales():
    models = Goods.query.all()

    return render_template('b_acc/sales.html', data=models)
