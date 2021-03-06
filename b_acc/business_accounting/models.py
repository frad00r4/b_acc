# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'


from ..exts import connection


class Nomenclatures(connection.Model):
    id = connection.Column(connection.Integer, primary_key=True)
    internal_code = connection.Column(connection.Integer, unique=True)
    name = connection.Column(connection.String(255))
    ext_name = connection.Column(connection.String(255), nullable=True)
    goods = connection.relationship('Goods', backref='nomenclature', lazy='dynamic')
    price = connection.relationship('Price', backref='nomenclature', lazy='dynamic')
    mysql_character_set = 'utf8'


class Documents(connection.Model):
    id = connection.Column(connection.Integer, primary_key=True)
    name = connection.Column(connection.String(255), unique=True)
    description = connection.Column(connection.String(255))
    incoming = connection.relationship('Incoming', backref='document', lazy='dynamic')
    actions = connection.relationship('AccountActions', backref='document', lazy='dynamic')
    mysql_character_set = 'utf8'


class Incoming(connection.Model):
    id = connection.Column(connection.Integer, primary_key=True)
    incoming_date = connection.Column(connection.DateTime, index=True)
    document_id = connection.Column(connection.Integer, connection.ForeignKey('documents.id'), nullable=False)
    account_id = connection.Column(connection.Integer, connection.ForeignKey('accounts.id'), nullable=False)
    paid = connection.Column(connection.Boolean, nullable=False, default=1)
    goods = connection.relationship('Goods', backref='incoming', lazy='dynamic')
    actions = connection.relationship('AccountActions', backref='incoming', lazy='dynamic')
    mysql_character_set = 'utf8'


class Goods(connection.Model):
    id = connection.Column(connection.Integer, primary_key=True)
    nomenclature_id = connection.Column(connection.Integer, connection.ForeignKey('nomenclatures.id'))
    attribute_id = connection.Column(connection.Integer, connection.ForeignKey('attributes.id'))
    incoming_id = connection.Column(connection.Integer, connection.ForeignKey('incoming.id'))
    incoming_date = connection.Column(connection.DateTime, index=True)
    outgoing_date = connection.Column(connection.DateTime, index=True)
    incoming_price = connection.Column(connection.Integer, nullable=False)
    outgoing_price = connection.Column(connection.Integer, nullable=False)
    paid = connection.Column(connection.Boolean, nullable=False, default=1)
    actions = connection.relationship('AccountActions', backref='goods', lazy='dynamic')
    mysql_character_set = 'utf8'


class Discounts(connection.Model):
    id = connection.Column(connection.Integer, primary_key=True)
    amount = connection.Column(connection.Integer, nullable=False)
    type = connection.Column(connection.Enum('strict', 'percent'), nullable=False)
    mysql_character_set = 'utf8'


class Attributes(connection.Model):
    id = connection.Column(connection.Integer, primary_key=True)
    name = connection.Column(connection.String(255), unique=True)
    goods = connection.relationship('Goods', backref='attribute', lazy='dynamic')
    price = connection.relationship('Price', backref='attribute', lazy='dynamic')
    mysql_character_set = 'utf8'


class Price(connection.Model):
    id = connection.Column(connection.Integer, primary_key=True)
    nomenclature_id = connection.Column(connection.Integer, connection.ForeignKey('nomenclatures.id'))
    attribute_id = connection.Column(connection.Integer, connection.ForeignKey('attributes.id'), nullable=True)
    price = connection.Column(connection.Integer, nullable=False)
    mysql_character_set = 'utf8'


class Accounts(connection.Model):
    id = connection.Column(connection.Integer, primary_key=True)
    name = connection.Column(connection.String(255), nullable=False, unique=True)
    total = connection.Column(connection.Integer, nullable=False)
    actived = connection.Column(connection.Boolean, nullable=False, default=1)
    incoming = connection.relationship('Incoming', backref='account', lazy='dynamic')
    actions = connection.relationship('AccountActions', backref='account', lazy='dynamic')
    mysql_character_set = 'utf8'


class AccountActions(connection.Model):
    id = connection.Column(connection.Integer, primary_key=True)
    account_id = connection.Column(connection.Integer, connection.ForeignKey('accounts.id'), nullable=False)
    document_id = connection.Column(connection.Integer, connection.ForeignKey('documents.id'), nullable=False)
    goods_id = connection.Column(connection.Integer, connection.ForeignKey('goods.id'), nullable=True)
    incoming_id = connection.Column(connection.Integer, connection.ForeignKey('incoming.id'), nullable=True)
    action_type = connection.Column(connection.Enum('incoming', 'outgoing'), nullable=False)
    amount = connection.Column(connection.Integer, nullable=False)
    datetime = connection.Column(connection.DateTime, nullable=False)
    mysql_character_set = 'utf8'
