# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask import Blueprint, request, render_template, flash, redirect, url_for
from .forms import AddNomenclatures
from .models import Nomenclatures
from ..exts import connection


business_accounting = Blueprint('b_acc', __name__, url_prefix='/b_acc/')


@business_accounting.route('nomenclatures')
def nomenclatures():
    nomenclatures = Nomenclatures.query.all()
    return render_template('b_acc/nomenclatures.html', nomenclatures=nomenclatures)


@business_accounting.route('nomenclatures/add', methods=('POST', 'GET'))
def add_nomenclature():
    form = AddNomenclatures()

    if request.method == 'POST' and form.validate():
        nomenclature = Nomenclatures(internal_code=int(form.internal_code.data),
                                     name=form.name.data,
                                     ext_name=form.ext_name.data)
        connection.session.add(nomenclature)
        try:
            connection.session.commit()
            flash(u'Номенклатура добавлена', 'success')
            return redirect(url_for('b_acc.nomenclatures'))
        except Exception as e:
            flash(u'Ошибка DB: %s' % e.message, 'danger')

    return render_template('b_acc/add_nomenclature.html', form=form)
