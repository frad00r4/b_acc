# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask import request, render_template, flash, redirect, url_for
from flask_wtf import Form
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
from ..models import Accounts
from ...exts import connection
from . import business_accounting


class AddAccount(Form):
    name = StringField(u'Название', validators=[DataRequired()])
    submit = SubmitField(u'Отправить')


@business_accounting.route('accounts')
def accounts():
    models = Accounts.query.all()
    print models
    return render_template('b_acc/accounts.html', accounts=models)


@business_accounting.route('accounts/add', methods=('POST', 'GET'))
def add_account():
    form = AddAccount()

    if request.method == 'POST' and form.validate():
        account = Accounts(name=form.name.data)
        connection.session.add(account)
        try:
            connection.session.commit()
            flash(u'Счет добавлен', 'success')
            return redirect(url_for('b_acc.accounts'))
        except Exception as e:
            flash(u'Ошибка DB: %s' % e.message, 'danger')

    return render_template('b_acc/add_account.html', form=form)
