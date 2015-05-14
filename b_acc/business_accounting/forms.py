# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'


from flask_wtf import Form
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired


class AddNomenclatures(Form):
    internal_code = IntegerField(u'Внутренний код', validators=[DataRequired()])
    name = StringField(u'Название', validators=[DataRequired()])
    ext_name = StringField(u'Дополнительная информация')
    submit = SubmitField(u'Отправить')
