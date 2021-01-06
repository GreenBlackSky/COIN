import logging
from functools import wraps

from nameko.rpc import rpc
from nameko_sqlalchemy import DatabaseSession
from .models import DeclarativeBase, TestData


def log_method(method):
    @wraps(method)
    def _wrapper(*args, **kargs):
        logging.debug(f"start {method.__name__} with {str(args)}, {str(kargs)}")
        ret = method(*args, **kargs)
        logging.debug(f"finish {method.__name__} with {str(args)}, {str(kargs)}, {str(ret)}")
        return ret
    return _wrapper


class DBService:
    name = "db_service"
    db = DatabaseSession(DeclarativeBase)

    @rpc
    @log_method
    def connection_test(self):
        return 'ok'

    @rpc
    @log_method
    def test_set_value(self, value):
        data = TestData(value=value)
        self.db.add(data)
        self.db.commit()
        return data.id

    @rpc
    @log_method
    def test_get_value(self, data_id):
        data = self.db.query(TestData).get(data_id)
        return data.value if data else None
