# -*- coding: utf-8 -*-

from flask import request, render_template, flash, redirect, url_for
from flask_wtf import Form
from wtforms import SubmitField, StringField, DateField, SelectField
from wtforms.validators import DataRequired
from sqlalchemy.sql.functions import func
from sqlalchemy.orm import aliased
from ...exts import connection
from ..utils import request_filter
from ..models import Accounts, AccountActions, Nomenclatures, Incoming, Goods
from . import business_accounting

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'


class AddAccount(Form):
    name = StringField(u'Название', validators=[DataRequired()])
    submit = SubmitField(u'Отправить')


class ActionsFilter(Form):
    from_date = DateField(u'От')
    to_date = DateField(u'До')
    action = SelectField(u'Операция', choices=[(0, u''),
                                               (1, u'Поступления'),
                                               (2, u'Расходы')], coerce=int)
    nomenclature_id = SelectField(u'Номенклатура', choices=[], coerce=int)
    incoming_id = SelectField(u'Поступление', choices=[], coerce=int)
    submit = SubmitField(u'Фильтровать')


@business_accounting.route('accounts', defaults={'page': 1})
@business_accounting.route('accounts/<int:page>')
def accounts(page):
    """
    SELECT
        accounts.id AS accounts_id,
        accounts.name AS accounts_name,
        accounts.actived AS accounts_actived,
        SUM(anon_1.amount) AS amount
    FROM
        accounts
            LEFT OUTER JOIN
        (SELECT
            anon_2.account_id AS account_id, anon_2.amount AS amount
        FROM
            (SELECT
            account_actions.account_id AS account_id,
                account_actions.amount AS amount
        FROM
            account_actions
        WHERE
            account_actions.action_type = 'incoming' UNION ALL SELECT
            account_actions.account_id AS account_id,
                account_actions.amount * - 1 AS anon_3
        FROM
            account_actions
        WHERE
            account_actions.action_type = 'outgoing') AS anon_2) AS anon_1 ON accounts.id = anon_1.account_id
    GROUP BY accounts.id
    """

    subreq_out = AccountActions.query. \
        with_entities(AccountActions.account_id.label('account_id'),
                      (AccountActions.amount.label('amount') * -1)). \
        filter_by(action_type='outgoing')

    total = AccountActions.query. \
        with_entities(AccountActions.account_id.label('account_id'),
                      AccountActions.amount.label('amount')). \
        filter_by(action_type='incoming'). \
        union_all(subreq_out). \
        subquery(name='total')

    subreq = aliased(total)

    accounts_req = Accounts.query. \
        with_entities(Accounts.id,
                      Accounts.name,
                      Accounts.actived,
                      func.sum(subreq.c.amount).label('amount')). \
        outerjoin(subreq). \
        group_by(Accounts.id)

    pagination = accounts_req.paginate(page, 10)
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
    account_model = Accounts.query.filter_by(id=account_id, actived=1).first()

    if not account_model:
        flash(u'Счет: %s не существует или уже закрыт' % account_id, 'danger')
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
    """
    SELECT
        accounts.id AS accounts_id,
        accounts.name AS accounts_name,
        accounts.actived AS accounts_actived,
        SUM(anon_1.amount) AS amount
    FROM
        accounts
            LEFT OUTER JOIN
        (SELECT
            anon_2.account_id AS account_id, anon_2.amount AS amount
        FROM
            (SELECT
            account_actions.account_id AS account_id,
                account_actions.amount AS amount
        FROM
            account_actions
        WHERE
            account_actions.action_type = 'incoming' UNION ALL SELECT
            account_actions.account_id AS account_id,
                account_actions.amount * - 1 AS anon_3
        FROM
            account_actions
        WHERE
            account_actions.action_type = 'outgoing') AS anon_2) AS anon_1 ON accounts.id = anon_1.account_id
    WHERE
        accounts.id = <account_id>
    GROUP BY accounts.id
    """

    data = request_filter(request.args,
                          filtered=['to_date', 'from_date', 'nomenclature_id', 'action', 'incoming_id'],
                          default=None)

    form = ActionsFilter(formdata=data)
    form.nomenclature_id.choices = [(0, u'')] + [(nom.id, "%d - %s" % (nom.internal_code, nom.name))
                                                 for nom in Nomenclatures.query.all()]
    form.incoming_id.choices = [(0, u'')] + [(incoming.id, incoming.incoming_date)
                                                 for incoming in Incoming.query.all()]

    req = AccountActions.query.filter_by(account_id=account_id)

    if form.from_date.data:
        req = req.filter(AccountActions.datetime > form.from_date.data)
    if form.to_date.data:
        req = req.filter(AccountActions.datetime < form.to_date.data)
    if form.nomenclature_id.data:
        req = req.filter(AccountActions.goods_id.in_([item.id for item in Goods.query.filter_by(nomenclature_id=form.nomenclature_id.data).all()]))
    if form.action.data:
        req = req.filter(AccountActions.action_type == ('incoming' if form.action.data == 1 else 'outgoing'))
    if form.incoming_id.data:
        req = req.filter(AccountActions.incoming_id == form.incoming_id.data)

    subreq_out = req. \
        with_entities(AccountActions.account_id.label('account_id'),
                      (AccountActions.amount.label('amount') * -1)). \
        filter_by(action_type='outgoing')

    total = req. \
        with_entities(AccountActions.account_id.label('account_id'),
                      AccountActions.amount.label('amount')). \
        filter_by(action_type='incoming'). \
        union_all(subreq_out). \
        subquery(name='total')

    subreq = aliased(total)

    account_model = Accounts.query. \
        filter_by(id=account_id). \
        with_entities(Accounts.id.label('account_id'),
                      Accounts.name,
                      Accounts.actived,
                      func.sum(subreq.c.amount).label('amount')). \
        outerjoin(subreq). \
        group_by(Accounts.id).first()
    if not account_model:
        flash(u'Счет: %s не существует' % account_id, 'danger')
        return redirect(url_for('b_acc.accounts'))

    pagination = req.order_by(AccountActions.datetime.desc()).paginate(page, 10)

    return render_template('b_acc/view_account.html', account=account_model, pagination=pagination, form=form)
