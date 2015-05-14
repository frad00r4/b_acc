# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask import Flask
from exts import connection, migrate, login_manager
from business_accounting import business_accounting
import os

BLUEPRINTS = (
    business_accounting,
)


__all__ = ('create_app', 'get_app')
app = None


def create_app(config=None):
    global app
    app = Flask('b_acc', static_url_path='/static',
                static_folder=os.path.join(os.path.dirname(__file__), '..', 'static'))
    print app._static_folder

    app.config.from_pyfile('config.py')
    if config:
        app.config.from_pyfile(config)

    init_exts(app)
    init_blueprints(app, BLUEPRINTS)

    return app


def init_exts(inst):
    connection.init_app(inst)
    migrate.init_app(inst, connection)
    login_manager.init_app(inst)


def init_blueprints(inst, blueprints):
    for bp in BLUEPRINTS:
        inst.register_blueprint(bp)


def get_app():
    global app
    return app


@login_manager.user_loader
def load_user(user_id):
    return 1