import logging
from functools import wraps

from flask import Blueprint, request

from . import rpc


def log_method(method):
    @wraps(method)
    def _wrapper(*args, **kargs):
        logging.debug(f"start {method.__name__} with {str(args)}, {str(kargs)}")
        ret = method(*args, **kargs)
        logging.debug(f"finish {method.__name__} with {str(args)}, {str(kargs)}, {str(ret)}")
        return ret
    return _wrapper


bp = Blueprint('test_bp', __name__)


@bp.route("/access_test", methods=['POST'])
@log_method
def access_test():
    return {'access': 'ok'}


@bp.route("/connection_test", methods=['POST'])
@log_method
def connection_test():
    redis_val = rpc.cache_service.connection_test()
    postgres_val = rpc.db_service.connection_test()
    return {'redis_val': redis_val, 'postgres_val': postgres_val}


@bp.route("/test_set_redis_value", methods=['POST'])
@log_method
def test_set_redis_value():
    key = request.args.get('key')
    val = request.args.get('val')
    rpc.cache_service.test_set_value(key, val)
    return {key: val}


@bp.route("/test_get_redis_value", methods=['POST'])
@log_method
def test_get_redis_value():
    key = request.args.get('key')
    val = rpc.cache_service.test_get_value(key)
    return {key: val}


@bp.route("/test_set_postgres_value", methods=['POST'])
@log_method
def test_set_postgres_value():
    val = request.args.get('val')
    key = rpc.db_service.test_set_value(val)
    return {key: val}


@bp.route("/test_get_postgres_value", methods=['POST'])
@log_method
def test_get_potgres_value():
    key = request.args.get('key')
    val = rpc.db_service.test_get_value(key)
    return {key: val}