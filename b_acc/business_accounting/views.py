# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask import Blueprint, request, render_template
from flask_login import login_required

business_accounting = Blueprint('b_acc', __name__, url_prefix='/b_acc/', template_folder='templates')


@business_accounting.route('add_nomenclature')
#@login_required
def add_nomenclature():
    if request.method == 'POST':
        pass

    return render_template('b_acc/add_nomenclature.html')
