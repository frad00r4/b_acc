# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask import render_template, flash, redirect, url_for
from sqlalchemy.sql.functions import func
from ..models import Goods, Nomenclatures, Attributes
from . import business_accounting


@business_accounting.route('storage', defaults={'page': 1})
@business_accounting.route('storage/<int:page>')
def storage(page):
    """
    SELECT
        goods.nomenclature_id AS goods_nomenclature_id,
        goods.attribute_id AS goods_attribute_id,
        goods.incoming_price AS goods_incoming_price,
        count(*) AS counts,
        attributes.name AS attr_name,
        nomenclatures.internal_code AS nomenclatures_internal_code,
        nomenclatures.name AS nom_name
    FROM goods
        JOIN nomenclatures ON nomenclatures.id = goods.nomenclature_id
        JOIN attributes ON attributes.id = goods.attribute_id
    WHERE
        goods.outgoing_date IS NULL AND
        goods.paid = 1
    GROUP BY
        goods.nomenclature_id,
        goods.attribute_id,
        goods.incoming_price
    """

    pagination = Goods.query.\
        with_entities(Goods.nomenclature_id,
                      func.count().label('counts'),
                      Nomenclatures.internal_code,
                      Nomenclatures.name.label('nom_name')).\
        join(Nomenclatures).\
        join(Attributes).\
        filter(func.isnull(Goods.outgoing_date), Goods.paid == True).\
        group_by(Goods.nomenclature_id).paginate(page, 10)

    return render_template('b_acc/storage.html', pagination=pagination)


@business_accounting.route('storage/attrs/<int:nomenclature_id>', defaults={'page': 1})
@business_accounting.route('storage/attrs/<int:nomenclature_id>/<int:page>')
def storage_attributes(nomenclature_id, page):
    """
    SELECT
        goods.nomenclature_id AS goods_nomenclature_id,
        goods.attribute_id AS goods_attribute_id,
        nomenclatures.internal_code AS nomenclatures_internal_code,
        nomenclatures.name AS nom_name,
        count(*) AS counts,
        goods.incoming_price AS goods_incoming_price,
        attributes.name AS attr_name
    FROM goods
        JOIN nomenclatures ON nomenclatures.id = goods.nomenclature_id
        JOIN attributes ON attributes.id = goods.attribute_id
    WHERE
        isnull(goods.outgoing_date) AND
        isnull(goods.outgoing_price) AND
        goods.nomenclature_id = :nomenclature_id_1
    GROUP BY
        goods.attribute_id,
        goods.incoming_price
    ORDER BY
        goods.attribute_id,
        goods.incoming_price
    """

    nomenclature = Nomenclatures.query.filter_by(id=nomenclature_id).first()

    if not nomenclature:
        flash(u'Аттрибуты и цены: номенклатуры не существует', 'danger')
        return redirect(url_for('b_acc.storage'))

    attributes = Goods.query.with_entities(Goods.nomenclature_id,
                                           Goods.attribute_id,
                                           Nomenclatures.internal_code,
                                           Nomenclatures.name.label('nom_name'),
                                           func.count().label('counts'),
                                           Goods.incoming_price,
                                           Attributes.name.label('attr_name')).\
        join(Nomenclatures).\
        join(Attributes).\
        filter(func.isnull(Goods.outgoing_date),
               func.isnull(Goods.outgoing_price),
               Goods.nomenclature_id == nomenclature_id).\
        group_by(Goods.attribute_id,
                 Goods.incoming_price).\
        order_by(Goods.attribute_id,
                 Goods.incoming_price)

    pagination = attributes.paginate(page, 10)

    return render_template('b_acc/storage_attributes.html', nomenclature=nomenclature, pagination=pagination)
