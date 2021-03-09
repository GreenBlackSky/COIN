"""Flask blueprint with test methods."""

import logging

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user

from common.debug_tools import log_function, log_request
from common.schemas import UserSchema

from . import rpc


bp = Blueprint('test_bp', __name__)


@bp.route("/test_login", methods=['POST'])
@jwt_required()
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
