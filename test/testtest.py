# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'

import unittest
from flask_testing import TestCase
from b_acc import get_app

class TestTest(TestCase):
    def create_app(self):
        app = get_app()
        return app

    def test_test(self):
        pass