# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask import request, render_template, flash, redirect, url_for
from flask_wtf import Form
from wtforms import SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired
from ..models import Discounts
from ...exts import connection
from . import business_accounting


class AddDiscount(Form):
    amount = IntegerField(u'Сумма скидки', validators=[DataRequired()])
    type = SelectField(u'Тип скидки', validators=[DataRequired()], choices=[(u'strict', u'Сумма скидки'),
                                                                            (u'percent', u'Процент')])
    submit = SubmitField(u'Отправить')


@business_accounting.route('discounts')
def discounts():
    models = Discounts.query.all()
    return render_template('b_acc/discounts.html', discounts=models)


@business_accounting.route('discounts/add', methods=('POST', 'GET'))
def add_discount():
    form = AddDiscount()

    if request.method == 'POST' and form.validate():
        discount = Discounts(amount=form.amount.data, type=form.type.data)
        connection.session.add(discount)
        try:
            connection.session.commit()
            flash(u'Скидка добавлена', 'success')
            return redirect(url_for('b_acc.discounts'))
        except Exception as e:
            flash(u'Ошибка DB: %s' % e.message, 'danger')

    return render_template('b_acc/add_discount.html', form=form)
