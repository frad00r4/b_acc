# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask import request, render_template, flash, redirect, url_for
from flask_wtf import Form
from wtforms import SubmitField, StringField
from wtforms.validators import DataRequired
from sqlalchemy.sql.functions import func
from ..models import Accounts, AccountActions
from ...exts import connection
from . import business_accounting


class AddAccount(Form):
    name = StringField(u'Название', validators=[DataRequired()])
    submit = SubmitField(u'Отправить')


@business_accounting.route('accounts', defaults={'page': 1})
@business_accounting.route('accounts/<int:page>')
def accounts(page):
    subreq_incoming = AccountActions.query.with_entities(func.sum(AccountActions.action_type).label('sum')).filter_by(action_type='incoming').cte()
    subreq_outgoing = AccountActions.query.with_entities(func.sum(AccountActions.action_type * -1).label('sum')).filter_by(action_type='outgoing').cte()
    connection.session.query()
    pagination = Accounts.query.filter_by(actived=1).paginate(page, 10)
    return render_template('b_acc/accounts.html', pagination=pagination)


@business_accounting.route('account/add', methods=('POST', 'GET'))
def add_account():
    form = AddAccount()

    if request.method == 'POST' and form.validate():
        account = Accounts(name=form.name.data,
                           total=0,
                           actived=1)
        connection.session.add(account)
        try:
            connection.session.commit()
            flash(u'Счет добавлен', 'success')
            return redirect(url_for('b_acc.accounts'))
        except Exception as e:
            flash(u'Ошибка DB: %s' % e.message, 'danger')

    return render_template('b_acc/add_account.html', form=form)


@business_accounting.route('account/<int:account_id>/del')
def del_account(account_id):
    account_model = Accounts.query.filter_by(id=account_id).first()

    if not account_model:
        flash(u'Счет: %s не существует' % account_id, 'danger')
    else:
        account_model.actived = 0

        try:
            connection.session.commit()
            flash(u'Счет закрыт', 'success')
        except Exception as e:
            flash(u'Ошибка DB: %s' % e.message, 'danger')

    return redirect(url_for('b_acc.accounts'))


@business_accounting.route('account/<int:account_id>', defaults={'page': 1})
@business_accounting.route('account/<int:account_id>/<int:page>')
def view_account(account_id, page):
    account_model = Accounts.query.filter_by(id=account_id).first()
    if not account_model:
        flash(u'Счет: %s не существует' % account_id, 'danger')
        return redirect(url_for('b_acc.accounts'))

    pagination = AccountActions.query.filter_by(account_id=account_id).paginate(page, 10)
    return render_template('b_acc/view_account.html', account=account_model, pagination=pagination)
