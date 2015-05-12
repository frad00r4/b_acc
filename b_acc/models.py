# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from pony.orm import *
from exts import connection

class Nomenclatures(connection.Entity):
    id = PrimaryKey(int, auto=True)
    internal_code = Required(int, size=32),
    name = Required(str, 255)
    ext_name = Required(str, 255)

class Documents(connection.Entity):
    id = PrimaryKey(int, auto=True)
    description = Required(str, 255)

class Goods_incoming(connection.Entity):
    id = PrimaryKey(int, auto=True)
    incoming_id = Required(int, size=32, index=True),
    nomenclature_id = Required('Nomenclatures')
    attribute_id = Required('Attributes')
    document_id = Optional('Documents')

class Attributes(connection.Entity):
    id = PrimaryKey(int, auto=True)
    name = Required(str, 255)
