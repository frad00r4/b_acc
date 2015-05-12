# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate

connection = SQLAlchemy()
migrate = Migrate()