# -*- coding: utf-8 -*-

from flask import request, render_template, flash, redirect, url_for
from flask_wtf import Form
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired
from ..models import Nomenclatures
from ...exts import connection
from . import business_accounting


__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'


class AddNomenclature(Form):
    internal_code = IntegerField(u'Внутренний код', validators=[DataRequired()])
    name = StringField(u'Название', validators=[DataRequired()])
    ext_name = StringField(u'Дополнительная информация')
    submit = SubmitField(u'Отправить')


@business_accounting.route('nomenclatures', defaults={'page': 1})
@business_accounting.route('nomenclatures/<int:page>')
def nomenclatures(page):
    pagination = Nomenclatures.query.order_by(Nomenclatures.internal_code.asc()).paginate(page, 10)
    return render_template('b_acc/nomenclatures.html', pagination=pagination)


@business_accounting.route('nomenclature/add', methods=('POST', 'GET'))
def add_nomenclature():
    form = AddNomenclature()

    if request.method == 'POST' and form.validate():
        nomenclature = Nomenclatures(internal_code=int(form.internal_code.data),
                                     name=form.name.data,
                                     ext_name=(form.ext_name.data if form.ext_name.data else None))
        connection.session.add(nomenclature)
        try:
            connection.session.commit()
            flash(u'Номенклатура добавлена', 'success')
            return redirect(url_for('b_acc.nomenclatures'))
        except Exception as e:
            flash(u'Ошибка DB: %s' % e.message, 'danger')

    return render_template('b_acc/add_nomenclature.html', form=form)


@business_accounting.route('nomenclature/<int:nomenclature_id>/edit', methods=('POST', 'GET'))
def edit_nomenclature(nomenclature_id):
    nomenclature = Nomenclatures.query.filter_by(id=nomenclature_id).first()

    if not nomenclature:
        flash(u'Номенклатуры %s не существует' % nomenclature_id, 'danger')
        return redirect(url_for('b_acc.nomenclatures'))
    form = AddNomenclature(obj=nomenclature)

    if request.method == 'POST' and form.validate():
        nomenclature.internal_code = int(form.internal_code.data)
        nomenclature.name = form.name.data
        nomenclature.ext_name = form.ext_name.data if form.ext_name.data else None

        try:
            connection.session.commit()
            flash(u'Номенклатура изменена', 'success')
            return redirect(url_for('b_acc.nomenclatures'))
        except Exception as e:
            flash(u'Ошибка DB: %s' % e.message, 'danger')

    return render_template('b_acc/add_nomenclature.html', form=form)
