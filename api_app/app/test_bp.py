"""Flask blueprint with test methods."""

import logging
from functools import wraps

from flask import Blueprint, request
from flask_login import login_required, current_user

from . import rpc


def log_method(method):
    """Decorate method for logging its input and output."""
    @wraps(method)
    def _wrapper(*args, **kargs):
        logging.debug(f"start {method.__name__}")
        ret = method(*args, **kargs)
        logging.debug(f"finish {method.__name__}")
        return ret
    return _wrapper


bp = Blueprint('test_bp', __name__)


@bp.route("/access_test", methods=['POST'])
@log_method
def access_test():
    """Ping."""
    return {'access': 'ok'}


@bp.route("/connection_test", methods=['POST'])
@log_method
def connection_test():
    """Check connection with cache and db services."""
    redis_val = rpc.cache_service.connection_test()
    postgres_val = rpc.db_service.connection_test()
    return {'redis_val': redis_val, 'postgres_val': postgres_val}


@bp.route("/test_set_redis_value", methods=['POST'])
@log_method
def test_set_redis_value():
    """Test method for setting value in redis."""
    key = request.args.get('key')
    val = request.args.get('val')
    rpc.cache_service.test_set_value(key, val)
    return {key: val}


@bp.route("/test_get_redis_value", methods=['POST'])
@log_method
def test_get_redis_value():
    """Test method for getting value from redis."""
    key = request.args.get('key')
    val = rpc.cache_service.test_get_value(key)
    return {key: val}


@bp.route("/test_set_postgres_value", methods=['POST'])
@log_method
def test_set_postgres_value():
    """Test method for setting value in postgres."""
    val = request.args.get('val')
    key = rpc.db_service.test_set_value(val)
    return {key: val}


@bp.route("/test_get_postgres_value", methods=['POST'])
@log_method
def test_get_potgres_value():
    """Test method for getting value in postgres."""
    key = request.args.get('key')
    val = rpc.db_service.test_get_value(key)
    return {key: val}


@bp.route("/test_login", methods=['POST'])
@login_required
@log_method
def test_login():
    """Test method for logged in user."""
    return {
        'status': "OK",
        'user_id': current_user.id
    }
