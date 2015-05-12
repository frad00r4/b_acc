#!/usr/bin/env python
# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

from flask_script import Manager
from flask_migrate import MigrateCommand
import unittest
import os

from b_acc import create_app
from b_acc.exts import connection

manager = Manager(create_app)
manager.add_command('db', MigrateCommand)

@manager.command
def init():
    connection.drop_all()
    connection.create_all()

@manager.command
def test():
    tests = unittest.defaultTestLoader.discover(os.path.join(os.getcwd(), 'test'))
    unittest.TextTestRunner().run(tests)

manager.add_option('-c', '--config', help='Config file', dest='config')

if __name__ == '__main__':
    manager.run()
