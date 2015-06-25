# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask import render_template, request
from ..models import Goods, Nomenclatures, Attributes
from flask_wtf import Form
from wtforms import SubmitField, DateTimeField, SelectField, IntegerField
from wtforms.validators import DataRequired
from . import business_accounting


class AddSale(Form):
    nomenclature_id = SelectField(u'Номенклатура', validators=[DataRequired()], choices=[], coerce=int)
    attribute_id = SelectField(u'Аттрибут', validators=[DataRequired()], choices=[], coerce=int)
    outgoing_date = DateTimeField(u'Дата продажи', validators=[DataRequired()])
    outgoing_price = IntegerField(u'Цена продажи', validators=[DataRequired()])
    submit = SubmitField(u'Отправить')


@business_accounting.route('sales')
def sales():
    models = Goods.query.all()

    return render_template('b_acc/sales.html', data=models)


@business_accounting.route('sale/add', methods=('POST', 'GET'))
def sale_add():
    form = AddSale()
    form.nomenclature_id.choices = [(nom.id, nom.internal_code) for nom in Nomenclatures.query.all()]
    form.attribute_id.choices = [(attr.id, attr.name) for attr in Attributes.query.all()]

    if request.method == 'POST' and form.validate():
        Goods.query.fliter()
        item = Goods.query.filter(Goods.incoming_date <= form.outgoing_date).\
            filter_by(nomenclature_id=form.nomenclature_id,
                      attribute_id=form.attribute_id,
                      outgoing_price=None,
                      outgoing_date=None).order_by(Goods.incoming_id.desc()).first()

