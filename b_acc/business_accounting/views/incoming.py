# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask import request, render_template, flash, redirect, url_for
from flask_wtf import Form
from wtforms import SubmitField, DateTimeField, SelectField, IntegerField
from wtforms.validators import DataRequired
from sqlalchemy.sql.functions import func
from ...exts import connection
from ..models import Incoming, Documents, Goods, Nomenclatures, Attributes
from . import business_accounting


class AddIncoming(Form):
    incoming_date = DateTimeField(u'Дата прихода', validators=[DataRequired()])
    document_id = SelectField(u'Документ', validators=[DataRequired()], choices=[], coerce=int)
    submit = SubmitField(u'Отправить')


class AddItem(Form):
    nomenclature_id = SelectField(u'Номенклатура', validators=[DataRequired()], choices=[], coerce=int)
    attribute_id = SelectField(u'Аттрибут', validators=[DataRequired()], choices=[], coerce=int)
    incoming_price = IntegerField(u'Цена прихода', validators=[DataRequired()])
    submit = SubmitField(u'Отправить')


@business_accounting.route('incoming')
def incoming():
    """
    SELECT
    incoming.id AS incoming_id,
    incoming.incoming_date AS incoming_incoming_date,
    (SELECT sum(goods.incoming_price) FROM goods WHERE goods.incoming_id = incoming.id) AS sum,
    documents.name AS documents_name
    FROM incoming JOIN documents ON documents.id = incoming.document_id
    """

    subreq = Goods.query.with_entities(func.sum(Goods.incoming_price)).filter_by(incoming_id=Incoming.id).subquery()
    models = Incoming.query.with_entities(Incoming.id,
                                          Incoming.incoming_date,
                                          subreq.as_scalar().label('sum'),
                                          Documents.name).join(Documents).all()

    return render_template('b_acc/incoming.html', data=models)


@business_accounting.route('incoming/add', methods=('POST', 'GET'))
def add_incoming():
    form = AddIncoming()
    form.document_id.choices = [(doc.id, doc.name) for doc in Documents.query.all()]

    if request.method == 'POST' and form.validate():
        incoming_obj = Incoming(incoming_date=form.incoming_date.data, document_id=form.document_id.data)
        connection.session.add(incoming_obj)
        try:
            connection.session.commit()
            flash(u'Поставка товара добавлена', 'success')
            return redirect(url_for('b_acc.incoming'))
        except Exception as e:
            flash(u'Ошибка DB: %s' % e.message, 'danger')

    return render_template('b_acc/add_incoming.html', form=form)


@business_accounting.route('incoming/<incoming_id>')
def view_incoming(incoming_id):
    model = Incoming.query.filter_by(id=incoming_id).first()
    if model:
        goods = Goods.query.filter_by(incoming_id=incoming_id).all()
        return render_template('b_acc/view_incoming.html', incoming=model, items=goods)
    else:
        flash(u'Поступления: %s не существует' % incoming_id, 'danger')
        return redirect(url_for('b_acc.incoming'))


@business_accounting.route('incoming/<incoming_id>/add', methods=('POST', 'GET'))
def view_incoming_append(incoming_id):
    incoming = Incoming.query.filter_by(id=incoming_id).first()

    if not incoming:
        flash(u'Поступления: %s не существует' % incoming_id, 'danger')
        return redirect(url_for('b_acc.incoming'))

    form = AddItem()
    form.nomenclature_id.choices = [(nom.id, nom.internal_code) for nom in Nomenclatures.query.all()]
    form.attribute_id.choices = [(attr.id, attr.name) for attr in Attributes.query.all()]

    if request.method == 'POST' and form.validate():
        item = Goods(nomenclature_id=form.nomenclature_id.data,
                     attribute_id=form.attribute_id.data,
                     incoming_id=incoming.id,
                     incoming_date=incoming.incoming_date,
                     outgoing_date=None,
                     incoming_price=form.incoming_price.data,
                     outgoing_price=None)
        connection.session.add(item)
        try:
            connection.session.commit()
            flash(u'Поставка товара добавлена', 'success')
            return redirect(url_for('b_acc.view_incoming', incoming_id=incoming.id))
        except Exception as e:
            flash(u'Ошибка DB: %s' % e.message, 'danger')

    return render_template('b_acc/view_incoming_append.html', form=form)


@business_accounting.route('incoming/<incoming_id>/<item_id>/edit', methods=('POST', 'GET'))
def edit_incoming_item(incoming_id, item_id):
    incoming = Incoming.query.filter_by(id=incoming_id).first()
    item = Goods.query.filter_by(id=item_id).first()

    if not incoming:
        flash(u'Поступления: %s не существует' % incoming_id, 'danger')
        return redirect(url_for('b_acc.incoming'))

    if not item:
        flash(u'Вещи: %s не существует' % item_id, 'danger')
        return redirect(url_for('b_acc.incoming', incoming_id=incoming.id))

    form = AddItem(obj=item)
    form.nomenclature_id.choices = [(nom.id, nom.internal_code) for nom in Nomenclatures.query.all()]
    form.attribute_id.choices = [(attr.id, attr.name) for attr in Attributes.query.all()]

    if request.method == 'POST' and form.validate():
        item.nomenclature_id = form.nomenclature_id.data,
        item.attribute_id = form.attribute_id.data,
        item.incoming_price = form.incoming_price.data,
        try:
            connection.session.commit()
            flash(u'Поставка товара изменена', 'success')
            return redirect(url_for('b_acc.view_incoming', incoming_id=incoming.id))
        except Exception as e:
            flash(u'Ошибка DB: %s' % e.message, 'danger')

    return render_template('b_acc/edit_incoming_item.html', form=form)


@business_accounting.route('incoming/<incoming_id>/<item_id>/del')
def del_incoming_item(incoming_id, item_id):
    incoming = Incoming.query.filter_by(id=incoming_id).first()
    item = Goods.query.filter_by(id=item_id).first()

    if not incoming:
        flash(u'Поступления: %s не существует' % incoming_id, 'danger')
        return redirect(url_for('b_acc.incoming'))

    if not item:
        flash(u'Вещи: %s не существует' % item_id, 'danger')
        return redirect(url_for('b_acc.incoming', incoming_id=incoming.id))

    connection.session.delete(item)
    try:
        connection.session.commit()
        flash(u'Поставка товара изменена - вещь удалена', 'success')
    except Exception as e:
        flash(u'Ошибка DB: %s' % e.message, 'danger')

    return redirect(url_for('b_acc.view_incoming', incoming_id=incoming.id))
