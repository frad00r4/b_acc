# -*- coding: utf-8 -*-


from flask import render_template, request, flash, redirect, url_for
from flask_wtf import Form
from wtforms import SelectField, SubmitField, IntegerField
from wtforms.validators import DataRequired
from ...exts import connection
from ..models import Price, Nomenclatures, Attributes
from . import business_accounting
import json


__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'


class PriceForm(Form):
    nomenclature_id = SelectField(u'Номенклатура', validators=[DataRequired()], choices=[], coerce=int)
    attribute_id = SelectField(u'Аттрибут', choices=[], coerce=int)
    price = IntegerField(u'Цена продажи', validators=[DataRequired()])
    submit = SubmitField(u'Отправить')


@business_accounting.route('prices', defaults={'page': 1})
@business_accounting.route('prices/<int:page>')
def prices(page):
    pagination = Price.query.join(Nomenclatures).order_by(Nomenclatures.internal_code.asc()).paginate(page, 10)
    return render_template('b_acc/price.html', pagination=pagination)


@business_accounting.route('price/add', methods=('POST', 'GET'))
def add_price():
    form = PriceForm()
    form.nomenclature_id.choices = [(nom.id, "%d - %s" % (nom.internal_code, nom.name))
                                    for nom in Nomenclatures.query.all()]
    form.attribute_id.choices = [(0, u'')] + [(attr.id, attr.name) for attr in Attributes.query.all()]

    if request.method == 'POST' and form.validate():
        price = Price(nomenclature_id=form.nomenclature_id.data,
                      attribute_id=None if form.attribute_id.data == 0 else form.attribute_id.data,
                      price=form.price.data)
        connection.session.add(price)

        try:
            connection.session.commit()
            flash(u'Цена установлена', 'success')
            return redirect(url_for('b_acc.prices'))
        except Exception as e:
            flash(u'Ошибка DB: %s' % e.message, 'danger')

    return render_template('b_acc/add_price.html', form=form)


@business_accounting.route('price/<int:price_id>/edit', methods=('POST', 'GET'))
def price_edit(price_id):
    price = Price.query.filter_by(id=price_id).first()

    if not price:
        flash(u'Цены: %s не существует' % price_id, 'danger')
        return redirect(url_for('b_acc.prices'))

    form = PriceForm(obj=price)
    form.attribute_id.data = 0 if price.attribute_id is None else price.attribute_id
    form.nomenclature_id.choices = [(nom.id, "%d - %s" % (nom.internal_code, nom.name))
                                    for nom in Nomenclatures.query.all()]
    form.attribute_id.choices = [(attr.id, attr.name) for attr in Attributes.query.all()]
    form.attribute_id.choices.append((0, u''))

    if request.method == 'POST' and form.validate():
        price.nomenclature_id = form.nomenclature_id.data
        price.attribute_id = None if form.attribute_id.data == 0 else form.attribute_id.data
        price.price = form.price.data

        try:
            connection.session.commit()
            flash(u'Цена товара изменена', 'success')
            return redirect(url_for('b_acc.prices'))
        except Exception as e:
            flash(u'Ошибка DB: %s' % e.message, 'danger')

    return render_template('b_acc/add_price.html', form=form)


@business_accounting.route('price/get')
def get_price():
    nomenclature = request.args.get('nomenclature', None)
    attribute = request.args.get('attribute', None)

    price_all = Price.query.filter_by(nomenclature_id=nomenclature,
                                      attribute_id=None).first()
    price = Price.query.filter_by(nomenclature_id=nomenclature,
                                  attribute_id=attribute).first() if attribute else None

    if price:
        return json.dumps({'result': True,
                           'nomenclature': price.nomenclature_id,
                           'attribute': price.attribute,
                           'price': price.price})
    elif price_all:
        return json.dumps({'result': True,
                           'nomenclature': price_all.nomenclature_id,
                           'attribute': price_all.attribute,
                           'price': price_all.price})
    else:
        return json.dumps({'result': False})


@business_accounting.route('price/<int:price_id>/del')
def del_price(price_id):
    price = Price.query.filter_by(id=price_id).first()

    if not price:
        flash(u'Цены: %s не существует' % price_id, 'danger')
    else:
        connection.session.delete(price)
        try:
            connection.session.commit()
            flash(u'Цена удалена', 'success')
        except Exception as e:
            flash(u'Ошибка DB: %s' % e.message, 'danger')

    return redirect(url_for('b_acc.prices'))
