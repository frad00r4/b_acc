# -*- coding: utf-8 -*-

from flask import render_template, request, redirect, url_for
from flask_wtf import Form
from wtforms import SubmitField, DateField
from werkzeug.datastructures import MultiDict
from sqlalchemy.sql.functions import func
from sqlalchemy.sql.expression import or_
from ..models import Goods, Accounts, AccountActions
from . import business_accounting


__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'


class ExistFilter(Form):
    on_date = DateField(u'На число')
    submit = SubmitField(u'Показать')


@business_accounting.route('report/exist')
def report_exist():
    req = Goods.query.\
        with_entities(func.sum(Goods.incoming_price).label('sum')).\
        filter(Goods.paid == True)

    data = dict()
    if request.args.get('on_date', None):
        data.update(on_date=request.args.get('on_date', None))
    form = ExistFilter(formdata=MultiDict(data))

    if form.on_date.data:
        req = req.filter(Goods.incoming_date <= form.on_date.data,
                         or_(Goods.outgoing_date > form.on_date.data,
                             func.isnull(Goods.outgoing_date)))
    else:
        req = req.filter(func.isnull(Goods.outgoing_price))

    return render_template('b_acc/report_exist.html', sum=req.first().sum, form=form)


@business_accounting.route('report/profit')
def report_profit():
    return 'STUB'