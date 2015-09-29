# -*- coding: utf-8 -*-

__author__ = 'frad00r4'
__email__ = 'frad00r4@gmail.com'


from werkzeug.datastructures import MultiDict
from models import Accounts
from ..exts import connection


def account_blocking(account_id, repeats=10):
    for i in range(repeats):
        account = Accounts.query.filter_by(id=account_id, blocking=False).with_for_update().first()
        if account:
            account.blocking = True
            connection.session.commit()
            return True

    return False


def request_filter(args, filtered=None, default=None):
    if not isinstance(filtered, list):
        return MultiDict(dict())

    data = dict()
    for item in filtered:
        if args.get(item, default):
            data.update({item: args.get(item, default)})

    return MultiDict(data)
