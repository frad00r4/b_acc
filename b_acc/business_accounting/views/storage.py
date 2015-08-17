# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask import render_template
from ..models import Goods
from ...exts import connection
from . import business_accounting


@business_accounting.route('storage', defaults={'page': 1})
@business_accounting.route('storage/<int:page>')
def storage(page):
    pagination = Goods.query.paginate(page, 1)
    print pagination.items
#    result = connection.engine.execute(
#            "SELECT n.internal_code AS internal_code, a.name AS attr_name, g.nomenclature_id, g.attribute_id, g.incoming_id, "
#            "g.incoming_price, count(*) AS counts FROM goods AS g JOIN nomenclatures AS n ON g.nomenclature_id = n.id "
#            "JOIN attributes AS a ON g.attribute_id = a.id WHERE ISNULL(g.outgoing_date) GROUP BY nomenclature_id, "
#            "attribute_id, incoming_id, incoming_price")

    return render_template('b_acc/storage.html', pagination=pagination)
