# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask import request, render_template, flash, redirect, url_for
from flask_wtf import Form
from wtforms import StringField, SubmitField
from wtforms.validators import DataRequired
from ..models import Attributes
from ...exts import connection
from . import business_accounting


class AddAttribute(Form):
    name = StringField(u'Название', validators=[DataRequired()])
    submit = SubmitField(u'Отправить')


@business_accounting.route('attributes', defaults={'page': 1})
@business_accounting.route('attributes/<int:page>')
def attributes(page):
    pagination = Attributes.query.paginate(page, 10)
    return render_template('b_acc/attributes.html', pagination=pagination)


@business_accounting.route('attributes/add', methods=('POST', 'GET'))
def add_attribute():
    form = AddAttribute()

    if request.method == 'POST' and form.validate():
        attribute = Attributes(name=form.name.data)
        connection.session.add(attribute)
        try:
            connection.session.commit()
            flash(u'Аттрибут добавлен', 'success')
            return redirect(url_for('b_acc.attributes'))
        except Exception as e:
            flash(u'Ошибка DB: %s' % e.message, 'danger')

    return render_template('b_acc/add_attribute.html', form=form)
