from flask import Blueprint

business_accounting = Blueprint('b_acc', __name__, url_prefix='/b_acc/')

import index
import nomenclatures
import documents
import attributes
import discounts
import accounts
import storage
import incoming
import sale
import investments
