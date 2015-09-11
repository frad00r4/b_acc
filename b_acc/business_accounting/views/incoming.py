# -*- coding: utf-8 -*-


from flask import request, render_template, flash, redirect, url_for
from flask_wtf import Form
from flask_wtf.file import FileField
from wtforms import SubmitField, DateTimeField, SelectField, IntegerField
from wtforms.validators import DataRequired
from sqlalchemy.sql.functions import func
from ...exts import connection
from ..models import Incoming, Documents, Goods, Nomenclatures, Attributes, Accounts, AccountActions
from . import business_accounting


__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'


class BadFile(Exception):
    pass


class AddIncoming(Form):
    incoming_date = DateTimeField(u'Дата прихода', validators=[DataRequired()])
    account_id = SelectField(u'Счет', validators=[DataRequired()], choices=[], coerce=int)
    document_id = SelectField(u'Документ', validators=[DataRequired()], choices=[], coerce=int)
    submit = SubmitField(u'Отправить')


class AddItem(Form):
    nomenclature_id = SelectField(u'Номенклатура', validators=[DataRequired()], choices=[], coerce=int)
    attribute_id = SelectField(u'Аттрибут', validators=[DataRequired()], choices=[], coerce=int)
    incoming_price = IntegerField(u'Цена прихода', validators=[DataRequired()])
    submit = SubmitField(u'Отправить')


class LoadIncoming(Form):
    csv_file = FileField(u'CSV файл', validators=[DataRequired()])
    submit = SubmitField(u'Отправить')


@business_accounting.route('incomings', defaults={'page': 1})
@business_accounting.route('incomings/<int:page>')
def incomings(page):
    """
    SELECT
        incoming.id AS incoming_id,
        incoming.incoming_date AS incoming_incoming_date,
        (SELECT sum(goods.incoming_price) FROM goods WHERE goods.incoming_id = incoming.id) AS sum,
        documents.name AS documents_name
    FROM incoming
        JOIN documents ON documents.id = incoming.document_id
    """

    subreq = Goods.query.with_entities(func.sum(Goods.incoming_price)).filter_by(incoming_id=Incoming.id).subquery()
    pagination = Incoming.query.with_entities(Incoming.id,
                                              Incoming.incoming_date,
                                              Incoming.paid,
                                              subreq.as_scalar().label('sum'),
                                              Documents.name).join(Documents).paginate(page, 10)

    return render_template('b_acc/incomings.html', pagination=pagination)


@business_accounting.route('incoming/add', methods=('POST', 'GET'))
def add_incoming():
    form = AddIncoming()
    form.document_id.choices = [(doc.id, doc.name) for doc in Documents.query.all()]
    form.account_id.choices = [(acc.id, acc.name) for acc in Accounts.query.filter_by(actived=1).all()]

    if request.method == 'POST' and form.validate():
        incoming_obj = Incoming(incoming_date=form.incoming_date.data,
                                document_id=form.document_id.data,
                                account_id=form.account_id.data,
                                paid=False)
        connection.session.add(incoming_obj)
        try:
            connection.session.commit()
            flash(u'Поставка товара добавлена', 'success')
            return redirect(url_for('b_acc.incomings'))
        except Exception as e:
            flash(u'Ошибка DB: %s' % e.message, 'danger')

    return render_template('b_acc/add_incoming.html', form=form)


@business_accounting.route('incoming/<int:incoming_id>/del')
def del_incoming(incoming_id):
    incoming_model = Incoming.query.filter_by(id=incoming_id, paid=False).first()
    item = Goods.query.filter_by(incoming_id=incoming_id).first()

    if not incoming_model:
        flash(u'Поступления: %s не существует или уже оплачено' % incoming_id, 'danger')
    elif item:
        flash(u'Поступление: %s от %s не пустое' % (incoming_model.id, incoming_model.incoming_date), 'danger')
    else:
        connection.session.delete(incoming_model)
        try:
            connection.session.commit()
            flash(u'Поступление удалено', 'success')
        except Exception as e:
            flash(u'Ошибка DB: %s' % e.message, 'danger')

    return redirect(url_for('b_acc.incomings'))


@business_accounting.route('incoming/<int:incoming_id>', defaults={'page': 1})
@business_accounting.route('incoming/<int:incoming_id>/<int:page>')
def view_incoming(incoming_id, page):
    model = Incoming.query.filter_by(id=incoming_id).first()
    if model:
        pagination = Goods.query.filter_by(incoming_id=incoming_id).paginate(page, 10)
        return render_template('b_acc/view_incoming.html', incoming=model, pagination=pagination)
    else:
        flash(u'Поступления: %s не существует' % incoming_id, 'danger')
        return redirect(url_for('b_acc.incomings'))


@business_accounting.route('incoming/<incoming_id>/add', methods=('POST', 'GET'))
def view_incoming_append(incoming_id):
    incoming_model = Incoming.query.filter_by(id=incoming_id, paid=False).first()

    if not incoming_model:
        flash(u'Поступления: %s не существует или уже оплачено' % incoming_id, 'danger')
        return redirect(url_for('b_acc.incomings'))

    form = AddItem()
    form.nomenclature_id.choices = [(nom.id, "%d - %s" % (nom.internal_code, nom.name))
                                    for nom in Nomenclatures.query.all()]
    form.attribute_id.choices = [(attr.id, attr.name) for attr in Attributes.query.all()]

    if request.method == 'POST' and form.validate():
        item = Goods(nomenclature_id=form.nomenclature_id.data,
                     attribute_id=form.attribute_id.data,
                     incoming_id=incoming_model.id,
                     incoming_date=incoming_model.incoming_date,
                     outgoing_date=None,
                     incoming_price=form.incoming_price.data,
                     outgoing_price=None,
                     paid=False)
        connection.session.add(item)
        try:
            connection.session.commit()
            flash(u'Поставка товара добавлена', 'success')
            return redirect(url_for('b_acc.view_incoming', incoming_id=incoming_model.id))
        except Exception as e:
            flash(u'Ошибка DB: %s' % e.message, 'danger')

    return render_template('b_acc/view_incoming_append.html', form=form)


@business_accounting.route('incoming/<int:incoming_id>/<int:item_id>/edit', methods=('POST', 'GET'))
def edit_incoming_item(incoming_id, item_id):
    incoming_model = Incoming.query.filter_by(id=incoming_id, paid=False).first()
    item = Goods.query.filter_by(id=item_id, paid=False).first()

    if not incoming_model:
        flash(u'Поступления: %s не существует или уже оплачено' % incoming_id, 'danger')
        return redirect(url_for('b_acc.incomings'))

    if not item:
        flash(u'Вещи: %s не существует' % item_id, 'danger')
        return redirect(url_for('b_acc.incomings', incoming_id=incoming_model.id))

    form = AddItem(obj=item)
    form.nomenclature_id.choices = [(nom.id, "%d - %s" % (nom.internal_code, nom.name))
                                    for nom in Nomenclatures.query.all()]
    form.attribute_id.choices = [(attr.id, attr.name) for attr in Attributes.query.all()]

    if request.method == 'POST' and form.validate():
        item.nomenclature_id = form.nomenclature_id.data
        item.attribute_id = form.attribute_id.data
        item.incoming_price = form.incoming_price.data
        try:
            connection.session.commit()
            flash(u'Поставка товара изменена', 'success')
            return redirect(url_for('b_acc.view_incoming', incoming_id=incoming_model.id))
        except Exception as e:
            flash(u'Ошибка DB: %s' % e.message, 'danger')

    return render_template('b_acc/edit_incoming_item.html', form=form)


@business_accounting.route('incoming/<int:incoming_id>/<int:item_id>/del')
def del_incoming_item(incoming_id, item_id):
    incoming_model = Incoming.query.filter_by(id=incoming_id, paid=False).first()
    item = Goods.query.filter_by(id=item_id).first()

    if not incoming_model:
        flash(u'Поступления: %s не существует или уже оплачено' % incoming_id, 'danger')
        return redirect(url_for('b_acc.incomings'))

    if not item:
        flash(u'Вещи: %s не существует' % item_id, 'danger')
        return redirect(url_for('b_acc.incomings', incoming_id=incoming_model.id))

    connection.session.delete(item)
    try:
        connection.session.commit()
        flash(u'Поставка товара изменена - вещь удалена', 'success')
    except Exception as e:
        flash(u'Ошибка DB: %s' % e.message, 'danger')

    return redirect(url_for('b_acc.view_incoming', incoming_id=incoming_model.id))


@business_accounting.route('incoming/<int:incoming_id>/pay')
def pay_incoming(incoming_id):
    incoming_model = Incoming.query.filter_by(id=incoming_id, paid=False).first()

    if not incoming_model:
        flash(u'Поступления: %s не существует или уже оплачено' % incoming_id, 'danger')
    else:
        incoming_model.paid = True

        Goods.query.filter_by(incoming_id=incoming_id).update({'paid': 1})

        total = Goods.query.with_entities(func.sum(Goods.incoming_price).label('sum')).\
            filter_by(incoming_id=incoming_id).first()
        action = AccountActions(account_id=incoming_model.account_id,
                                document_id=incoming_model.document_id,
                                action_type='outgoing',
                                amount=total.sum,
                                datetime=incoming_model.incoming_date,
                                incoming_id=incoming_model.id)
        connection.session.add(action)

        try:
            connection.session.commit()
            flash(u'Поступление оплачено', 'success')
        except Exception as e:
            connection.session.rollback()
            flash(u'Ошибка DB: %s' % e.message, 'danger')

    return redirect(url_for('b_acc.incomings'))


@business_accounting.route('incoming/<int:incoming_id>/load', methods=('POST', 'GET'))
def load_incoming(incoming_id):
    incoming_model = Incoming.query.filter_by(id=incoming_id, paid=False).first()

    if not incoming_model:
        flash(u'Поступления: %s не существует или уже оплачено' % incoming_id, 'danger')
        return redirect(url_for('b_acc.incomings'))

    form = LoadIncoming()

    if request.method == 'POST' and form.validate():
        try:
            nomenclatures = dict()
            attributes = dict()
            for row_raw in form.csv_file.data:
                if unicode(row_raw).strip():
                    row = unicode(row_raw).strip().split(';')
                    if len(row) != 4:
                        raise BadFile(u'Bad row %s' % unicode(row_raw))
                    attrs = row[2].split(',')
                    if len(attrs) != int(row[1]):
                        raise BadFile(u'Кол-во размеров не равноу указанному кол-ву товара (%s)' % unicode(row_raw))

                    if row[0] not in nomenclatures:
                        nomenclature = Nomenclatures.query.filter_by(internal_code=int(row[0])).first()
                        if not nomenclature:
                            raise BadFile(u'Нет такой номенклатуры %s' % unicode(row_raw))
                        nomenclatures.update({row[0]: nomenclature.id})

                    for attr in attrs:
                        if attr not in attributes:
                            attribute = Attributes.query.filter_by(id=int(attr)).first()
                            if not attribute:
                                raise BadFile(u'Нет такого аттрибута %s' % unicode(row_raw))
                            attributes.update({attr: attribute.id})

                        item = Goods(nomenclature_id=nomenclatures[row[0]],
                                     attribute_id=attributes[attr],
                                     incoming_id=incoming_model.id,
                                     incoming_date=incoming_model.incoming_date,
                                     outgoing_date=None,
                                     incoming_price=int(row[3]),
                                     outgoing_price=None,
                                     paid=False)
                        connection.session.add(item)

            try:
                connection.session.commit()
                flash(u'Поставка товара добавлена', 'success')
                return redirect(url_for('b_acc.view_incoming', incoming_id=incoming_model.id))
            except Exception as e:
                flash(u'Ошибка DB: %s' % e.message, 'danger')

        except BadFile as e:
            flash(u'Ошибка в CSV: %s' % e.message, 'danger')

    return render_template('b_acc/load_incoming.html', form=form)
