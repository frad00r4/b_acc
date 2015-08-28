# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask import request, render_template, flash, redirect, url_for
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from ..models import Documents
from ...exts import connection
from . import business_accounting

class AddDocument(Form):
    name = StringField(u'Название', validators=[DataRequired()])
    description = StringField(u'Описание документа')
    submit = SubmitField(u'Отправить')


@business_accounting.route('documents', defaults={'page': 1})
@business_accounting.route('documents/<int:page>')
def documents(page):
    pagination = Documents.query.paginate(page, 10)
    return render_template('b_acc/documents.html', pagination=pagination)


@business_accounting.route('documents/add', methods=('POST', 'GET'))
def add_document():
    form = AddDocument()

    if request.method == 'POST' and form.validate():
        document = Documents(name=form.name.data, description=form.description.data)
        connection.session.add(document)
        try:
            connection.session.commit()
            flash(u'Документ добавлен', 'success')
            return redirect(url_for('b_acc.documents'))
        except Exception as e:
            flash(u'Ошибка DB: %s' % e.message, 'danger')

    return render_template('b_acc/add_document.html', form=form)