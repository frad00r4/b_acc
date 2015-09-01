# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask import render_template, request, flash, redirect, url_for
from sqlalchemy.sql.functions import func
from flask_wtf import Form
from wtforms import SubmitField, DateTimeField, SelectField, IntegerField, DateField
from wtforms.validators import DataRequired
from ..models import Goods, Nomenclatures, Attributes, Documents, Accounts, AccountActions
from ...exts import connection
from . import business_accounting
from werkzeug.datastructures import MultiDict


class AddSale(Form):
    nomenclature_id = SelectField(u'Номенклатура', validators=[DataRequired()], choices=[], coerce=int)
    attribute_id = SelectField(u'Аттрибут', validators=[DataRequired()], choices=[], coerce=int)
    document_id = SelectField(u'Документ', validators=[DataRequired()], choices=[], coerce=int)
    account_id = SelectField(u'Счет', validators=[DataRequired()], choices=[], coerce=int)
    outgoing_date = DateTimeField(u'Дата продажи', validators=[DataRequired()])
    outgoing_price = IntegerField(u'Цена продажи', validators=[DataRequired()])
    submit = SubmitField(u'Отправить')


class SalesFilter(Form):
    from_date = DateField(u'От')
    to_date = DateField(u'До')
    nomenclature_id = SelectField(u'Номенклатура', choices=[], coerce=int)
    attribute_id = SelectField(u'Аттрибут', choices=[], coerce=int)
    submit = SubmitField(u'Фильтровать')


@business_accounting.route('sales', defaults={'page': 1})
@business_accounting.route('sales/<int:page>')
def sales(page):
    data = dict()
    if request.args.get('to_date', None):
        data.update(to_date=request.args.get('to_date', None))
    if request.args.get('from_date', None):
        data.update(from_date=request.args.get('from_date', None))
    if request.args.get('nomenclature_id', None):
        data.update(nomenclature_id=request.args.get('nomenclature_id', None))
    if request.args.get('attribute_id', None):
        data.update(attribute_id=request.args.get('attribute_id', None))

    form = SalesFilter(formdata=MultiDict(data))
    form.nomenclature_id.choices = [(0, u'')] + [(nom.id, "%d - %s" % (nom.internal_code, nom.name))
                                    for nom in Nomenclatures.query.all()]
    form.attribute_id.choices = [(0, u'')] + [(attr.id, attr.name) for attr in Attributes.query.all()]

    req = Goods.query.filter(Goods.outgoing_price != None, Goods.outgoing_date != None).\
        order_by(Goods.outgoing_date.desc())

    sales_sum = Goods.query.with_entities(func.sum(Goods.outgoing_price).label('sum')).\
        filter(Goods.outgoing_price != None, Goods.outgoing_date != None)

    if form.from_date.data:
        req = req.filter(Goods.outgoing_date > form.from_date.data)
        sales_sum = sales_sum.filter(Goods.outgoing_date > form.from_date.data)
    if form.to_date.data:
        req = req.filter(Goods.outgoing_date < form.to_date.data)
        sales_sum = sales_sum.filter(Goods.outgoing_date < form.to_date.data)
    if form.nomenclature_id.data:
        req = req.filter(Goods.nomenclature_id == form.nomenclature_id.data)
        sales_sum = sales_sum.filter(Goods.nomenclature_id == form.nomenclature_id.data)
    if form.attribute_id.data:
        req = req.filter(Goods.attribute_id == form.attribute_id.data)
        sales_sum = sales_sum.filter(Goods.attribute_id == form.attribute_id.data)

    pagination = req.paginate(page, 10)
    return render_template('b_acc/sales.html',
                           pagination=pagination,
                           sum=sales_sum.first().sum,
                           form=form)


@business_accounting.route('sale/add', methods=('POST', 'GET'))
def sale_add():
    form = AddSale()
    form.nomenclature_id.choices = [(nom.id, "%d - %s" % (nom.internal_code, nom.name))
                                    for nom in Nomenclatures.query.all()]
    form.attribute_id.choices = [(attr.id, attr.name) for attr in Attributes.query.all()]
    form.document_id.choices = [(doc.id, doc.name) for doc in Documents.query.all()]
    form.account_id.choices = [(acc.id, acc.name) for acc in Accounts.query.filter_by(actived=1).all()]

    if request.method == 'POST' and form.validate():
        account = Accounts.query.filter_by(id=form.account_id.data, actived=1).first()
        item = Goods.query.filter(Goods.incoming_date < form.outgoing_date.data.strftime('%Y-%m-%d %H:%M:%S')).\
            filter_by(nomenclature_id=form.nomenclature_id.data,
                      attribute_id=form.attribute_id.data,
                      outgoing_price=None,
                      outgoing_date=None).order_by(Goods.incoming_id.desc()).first()

        if not account:
            flash(u'Продажа: нет такого счета или он закрыт: %d' % form.account_id.data, 'danger')
        elif not item:
            flash(u'Продажа: нет подходящего товара, по заданным критериям', 'danger')
        else:
            action = AccountActions(account_id=form.account_id.data,
                                    document_id=form.document_id.data,
                                    goods_id=item.id,
                                    action_type='incoming',
                                    amount=form.outgoing_price.data,
                                    datetime=form.outgoing_date.data)
            connection.session.add(action)

            item.outgoing_price = form.outgoing_price.data
            item.outgoing_date = form.outgoing_date.data.strftime('%Y-%m-%d %H:%M:%S')

            account.total += form.outgoing_price.data

            try:
                connection.session.commit()
                flash(u'Поставка товара добавлена', 'success')
                return redirect(url_for('b_acc.sales'))
            except Exception as e:
                flash(u'Ошибка DB: %s' % e.message, 'danger')

    return render_template('b_acc/add_sale.html', form=form)
