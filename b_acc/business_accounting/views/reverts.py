# -*- coding: utf-8 -*-

from flask import render_template, request, flash, redirect, url_for
from flask_wtf import Form
from wtforms import SubmitField, DateTimeField, SelectField, IntegerField
from wtforms.validators import DataRequired
from ..models import Goods, Nomenclatures, Attributes, Documents, Accounts, AccountActions
from ...exts import connection
from . import business_accounting


__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'


class AddRevert(Form):
    nomenclature_id = SelectField(u'Номенклатура', validators=[DataRequired()], choices=[], coerce=int)
    attribute_id = SelectField(u'Аттрибут', validators=[DataRequired()], choices=[], coerce=int)
    document_id = SelectField(u'Документ', validators=[DataRequired()], choices=[], coerce=int)
    account_id = SelectField(u'Счет', validators=[DataRequired()], choices=[], coerce=int)
    outgoing_date = DateTimeField(u'Дата продажи', validators=[DataRequired()])
    outgoing_price = IntegerField(u'Цена продажи', validators=[DataRequired()])
    revert_date = DateTimeField(u'Дата возврата', validators=[DataRequired()])
    submit = SubmitField(u'Отправить')


@business_accounting.route('revert/add', methods=('POST', 'GET'))
def revert_add():
    form = AddRevert()
    form.nomenclature_id.choices = [(nom.id, "%d - %s" % (nom.internal_code, nom.name))
                                    for nom in Nomenclatures.query.all()]
    form.attribute_id.choices = [(attr.id, attr.name) for attr in Attributes.query.all()]
    form.document_id.choices = [(doc.id, doc.name) for doc in Documents.query.all()]
    form.account_id.choices = [(acc.id, acc.name) for acc in Accounts.query.filter_by(actived=1).all()]

    if request.method == 'POST' and form.validate():
        account = Accounts.query.filter_by(id=form.account_id.data, actived=1).first()
        item = Goods.query.filter_by(nomenclature_id=form.nomenclature_id.data,
                                     attribute_id=form.attribute_id.data,
                                     outgoing_date=form.outgoing_date.data.strftime('%Y-%m-%d %H:%M:%S'),
                                     outgoing_price=form.outgoing_price.data,
                                     paid=True).order_by(Goods.incoming_id.desc()).first()

        if not account:
            flash(u'Продажа: нет такого счета или он закрыт: %d' % form.account_id.data, 'danger')
        elif not item:
            flash(u'Продажа: нет подходящего товара, по заданным критериям', 'danger')
        else:
            action = AccountActions(account_id=form.account_id.data,
                                    document_id=form.document_id.data,
                                    goods_id=item.id,
                                    action_type='outgoing',
                                    amount=form.outgoing_price.data,
                                    datetime=form.revert_date.data)
            connection.session.add(action)

            item.outgoing_price = None
            item.outgoing_date = None

            try:
                connection.session.commit()
                flash(u'Возврат оформлен', 'success')
                return redirect(url_for('b_acc.accounts'))
            except Exception as e:
                flash(u'Ошибка DB: %s' % e.message, 'danger')

    return render_template('b_acc/add_revert.html', form=form)
