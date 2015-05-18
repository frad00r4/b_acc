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
    description = connection.Column(connection.String(255))


class GoodsIncoming(connection.Model):
    id = connection.Column(connection.Integer, primary_key=True)
    incoming_id = connection.Column(connection.Integer, index=True)
    nomenclature_id = connection.Column(connection.Integer, connection.ForeignKey('nomenclatures.id'))
    attribute_id = connection.Column(connection.Integer, connection.ForeignKey('attributes.id'))
    document_id = connection.Column(connection.Integer, connection.ForeignKey('documents.id'), nullable=False)


class Attributes(connection.Model):
    id = connection.Column(connection.Integer, primary_key=True)
    name = connection.Column(connection.String(255))
