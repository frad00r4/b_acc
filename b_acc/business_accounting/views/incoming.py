# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask import request, render_template, flash, redirect, url_for
from flask_wtf import Form
from wtforms import SubmitField, DateTimeField, SelectField, IntegerField
from wtforms.validators import DataRequired
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
    models = Incoming.query.all()
    return render_template('b_acc/incoming.html', data=models)


@business_accounting.route('incoming/add', methods=('POST', 'GET'))
def add_incoming():
    documents = [(doc.id, doc.name) for doc in Documents.query.all()]
    form = AddIncoming()
    form.document_id.choices = documents

    if request.method == 'POST' and form.validate():
        incoming = Incoming(incoming_date=form.incoming_date.data, document_id=form.document_id.data)
        connection.session.add(incoming)
        try:
            connection.session.commit()
            flash(u'Поставка товара добавлена', 'success')
            return redirect(url_for('b_acc.incoming'))
        except Exception as e:
            flash(u'Ошибка DB: %s' % e.message, 'danger')

    return render_template('b_acc/add_incoming.html', form=form)


@business_accounting.route('incoming/<incoming_id>')
def view_incoming(incoming_id):
    incoming = Incoming.query.filter_by(id=incoming_id).first()
    if incoming:
        goods = Goods.query.filter_by(incoming_id=incoming_id).all()
        return render_template('b_acc/view_incoming.html', incoming=incoming, items=goods)
    else:
        flash(u'Поступления: %s не существует' % incoming_id, 'danger')
        return redirect(url_for('b_acc.incoming'))

@business_accounting.route('incoming/<incoming_id>/add', methods=('POST', 'GET'))
def view_incoming_append(incoming_id):
    incoming = Incoming.query.filter_by(id=incoming_id).first()

    if incoming:

        form = AddItem()
        nomenclatures = [(nom.id, nom.internal_code) for nom in Nomenclatures.query.all()]
        attributes = [(attr.id, attr.name) for attr in Attributes.query.all()]
        form.nomenclature_id.choices = nomenclatures
        form.attribute_id.choices = attributes

        if request.method == 'POST' and form.validate():
            item = Goods(nomenclature_id = form.nomenclature_id.data,
                         attribute_id = form.attribute_id.data,
                         incoming_id = incoming.id,
                         incoming_date = incoming.incoming_date,
                         outgoing_date = None,
                         incoming_price = form.incoming_price.data,
                         outgoing_price = None)
            connection.session.add(item)
            try:
                connection.session.commit()
                flash(u'Поставка товара добавлена', 'success')
                return redirect(url_for('b_acc.view_incoming', incoming_id=incoming.id))
            except Exception as e:
                flash(u'Ошибка DB: %s' % e.message, 'danger')

        return render_template('b_acc/view_incoming_append.html', form=form)

    else:
        flash(u'Поступления: %s не существует' % incoming_id, 'danger')
        return redirect(url_for('b_acc.incoming'))
