# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask import Blueprint, request, render_template
from .forms import AddNomenclatures

business_accounting = Blueprint('b_acc', __name__, url_prefix='/b_acc/')


@business_accounting.route('add_nomenclature', methods=('POST', 'GET'))
def add_nomenclature():
    form = AddNomenclatures()

    if request.method == 'POST':
        if form.validate_on_submit():
            return 'GOOD'

    return render_template('b_acc/add_nomenclature.html', form=form)
