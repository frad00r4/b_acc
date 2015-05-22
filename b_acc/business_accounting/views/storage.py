# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask import request, render_template, flash, redirect, url_for
from ..models import Goods, Nomenclatures, Attributes, Incoming
from ...exts import connection
from . import business_accounting


@business_accounting.route('storage')
def storage():
    models = Goods.query.paginate(1,3)
    print models
    #return render_template('b_acc/storage.html', goods=models)
    return 'TEST'
