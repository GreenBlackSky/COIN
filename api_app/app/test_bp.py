"""Flask blueprint with test methods."""

import logging

from flask import Blueprint, request
from flask_login import login_required, current_user

from common.debug_tools import log_method, log_request
from common.schemas import UserSchema

from . import rpc


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
@log_request
def test_set_redis_value():
    """Test method for setting value in redis."""
    key = request.args.get('key')
    val = request.args.get('val')
    rpc.cache_service.test_set_value(key, val)
    return {key: val}


@bp.route("/test_get_redis_value", methods=['POST'])
@log_request
def test_get_redis_value():
    """Test method for getting value from redis."""
    key = request.args.get('key')
    val = rpc.cache_service.test_get_value(key)
    return {key: val}


@bp.route("/test_set_postgres_value", methods=['POST'])
@log_request
def test_set_postgres_value():
    """Test method for setting value in postgres."""
    val = request.args.get('val')
    key = rpc.db_service.test_set_value(val)
    return {key: val}


@bp.route("/test_get_postgres_value", methods=['POST'])
@log_request
def test_get_potgres_value():
    """Test method for getting value in postgres."""
    key = request.args.get('key')
    val = rpc.db_service.test_get_value(key)
    return {key: val}


@bp.route("/test_login", methods=['POST'])
@login_required
@log_request
def test_login():
    """Test method for logged in user."""
    return {
        'status': "OK",
        'user_id': current_user.id
    }


@bp.route("/clear_users", methods=['POST'])
@log_request
def clear():
    """Clear all users from db and clear cache."""
    rpc.cache_service.clear()
    count = rpc.db_service.clear_users()
    return {"users removed": count}
