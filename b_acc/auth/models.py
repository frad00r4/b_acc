# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'


from ..exts import connection
from flask_login import UserMixin

class Users(connection.Model, UserMixin):
    __tablename__ = 'users'
    id = connection.Column(connection.Integer, primary_key=True)
    name = connection.Column(connection.String(255))
    password = connection.Column(connection.String(255))
