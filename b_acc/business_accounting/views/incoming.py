# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask import request, render_template, flash, redirect, url_for
from flask_wtf import Form
from wtforms import SubmitField, DateTimeField, SelectField
from wtforms.validators import DataRequired
from ...exts import connection
from ..models import Incoming, Documents
from . import business_accounting


class AddIncoming(Form):
    incoming_date = DateTimeField(u'Дата прихода', validators=[DataRequired()])

    document_id = SelectField(u'Документ', validators=[DataRequired()], choices=[], coerce=int)
    submit = SubmitField(u'Отправить')


@business_accounting.route('goods_incoming')
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


@business_accounting.route('incoming/<incoming_id>', methods=('POST', 'GET'))
def view_incoming(incoming_id):
    incoming = Incoming.query.filter_by(id=incoming_id).first()
    if incoming:
        return render_template('b_acc/incoming.html', incoming=incoming)
    else:
        flash(u'Поступления: %s не существует' % incoming_id, 'danger')
        return redirect(url_for('b_acc.incoming'))
