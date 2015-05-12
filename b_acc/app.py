# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask import Flask
from exts import connection, migrate

__all__ = ('create_app', 'get_app')
app = None

def create_app(config=None):
    global app
    app = Flask('b_acc')

    app.config.from_pyfile('config.py')
    if config:
        app.config.from_pyfile(config)

    connection.init_app(app)
    migrate.init_app(app, connection)

    return app

def get_app():
    global app
    return app