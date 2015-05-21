# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'


from ..exts import connection


class Nomenclatures(connection.Model):
    id = connection.Column(connection.Integer, primary_key=True)
    internal_code = connection.Column(connection.Integer, unique=True)
    name = connection.Column(connection.String(255))
    ext_name = connection.Column(connection.String(255), nullable=True)


class Documents(connection.Model):
    id = connection.Column(connection.Integer, primary_key=True)
    name = connection.Column(connection.String(255), unique=True)
    description = connection.Column(connection.String(255))


class Incoming(connection.Model):
    id = connection.Column(connection.Integer, primary_key=True)
    incoming_date = connection.Column(connection.DateTime, index=True)
    document_id = connection.Column(connection.Integer, connection.ForeignKey('documents.id'), nullable=False)


class Goods(connection.Model):
    id = connection.Column(connection.Integer, primary_key=True)
    nomenclature_id = connection.Column(connection.Integer, connection.ForeignKey('nomenclatures.id'))
    attribute_id = connection.Column(connection.Integer, connection.ForeignKey('attributes.id'))
    incoming_id = connection.Column(connection.Integer, connection.ForeignKey('incoming.id'))
    incoming_date = connection.Column(connection.DateTime, index=True)
    outgoing_date = connection.Column(connection.DateTime, index=True)
    incoming_price = connection.Column(connection.Integer, nullable=False)
    outgoing_price = connection.Column(connection.Integer, nullable=False)


class Discounts(connection.Model):
    id = connection.Column(connection.Integer, primary_key=True)
    amount = connection.Column(connection.Integer, nullable=False)
    type = connection.Column(connection.Enum('strict', 'percent'), nullable=False)


class Attributes(connection.Model):
    id = connection.Column(connection.Integer, primary_key=True)
    name = connection.Column(connection.String(255), unique=True)


class Price(connection.Model):
    id = connection.Column(connection.Integer, primary_key=True)
    goods_id = connection.Column(connection.Integer, connection.ForeignKey('goods.id'))
    attribute_id = connection.Column(connection.Integer, connection.ForeignKey('attributes.id'), nullable=True)
    price = connection.Column(connection.Integer, nullable=False)


class Accounts(connection.Model):
    id = connection.Column(connection.Integer, primary_key=True)
    name = connection.Column(connection.String(255), nullable=False, unique=True)


class AccountsActions(connection.Model):
    id = connection.Column(connection.Integer, primary_key=True)
    account_id = connection.Column(connection.Integer, connection.ForeignKey('accounts.id'), nullable=False)
    document_id = connection.Column(connection.Integer, connection.ForeignKey('documents.id'), nullable=False)
    goods_id = connection.Column(connection.Integer, connection.ForeignKey('goods.id'), nullable=True)
    action_type = connection.Column(connection.Enum('incoming', 'outgoing'), nullable=False)
    amount = connection.Column(connection.Integer, nullable=False)