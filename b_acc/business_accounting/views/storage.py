# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask import render_template
from ..models import Goods
from . import business_accounting


@business_accounting.route('storage', defaults={'page': 1})
@business_accounting.route('storage/<int:page>')
def storage(page):
    pagination = Goods.query.paginate(page, 1)
    print pagination.items

    return render_template('b_acc/storage.html', pagination=pagination)
