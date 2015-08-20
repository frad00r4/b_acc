# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask import request, render_template, flash, redirect, url_for
from flask_wtf import Form
from wtforms import SubmitField, SelectField, IntegerField, DateTimeField
from wtforms.validators import DataRequired
from ..models import AccountActions, Documents, Accounts
from ...exts import connection
from . import business_accounting


class AddInvestments(Form):
    datetime = DateTimeField(u'Дата прихода', validators=[DataRequired()])
    account_id = SelectField(u'Счет', validators=[DataRequired()], choices=[], coerce=int)
    document_id = SelectField(u'Документ', validators=[DataRequired()], choices=[], coerce=int)
    amount = IntegerField(u'Сумма прихода', validators=[DataRequired()])
    submit = SubmitField(u'Отправить')


@business_accounting.route('investments', methods=('POST', 'GET'))
def investments():
    form = AddInvestments()
    form.document_id.choices = [(doc.id, doc.name) for doc in Documents.query.all()]
    form.account_id.choices = [(acc.id, acc.name) for acc in Accounts.query.filter_by(actived=1).all()]

    if request.method == 'POST' and form.validate():
        account = Accounts.query.filter_by(id=form.account_id.data, actived=1).first()

        if not account:
            flash(u'Инвестиции: нет такого счета или он закрыт: %d' % form.account_id.data, 'danger')
        else:
            investment = AccountActions(account_id=form.account_id.data,
                                        document_id=form.document_id.data,
                                        action_type='incoming',
                                        amount=form.amount.data,
                                        datetime=form.datetime.data)
            connection.session.add(investment)

            try:
                connection.session.commit()
                flash(u'Инвестиция добавлена', 'success')
                return redirect(url_for('b_acc.accounts'))
            except Exception as e:
                flash(u'Ошибка DB: %s' % e.message, 'danger')

    return render_template('b_acc/investments.html', form=form)
