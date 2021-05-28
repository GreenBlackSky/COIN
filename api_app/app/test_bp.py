"""Flask blueprint with test methods."""

from time import sleep

from flask import Blueprint
from flask_jwt_extended import jwt_required, current_user

from common.debug_tools import wrap_request

from . import rpc
from .model import session, UserModel


bp = Blueprint('test_bp', __name__)


@bp.route("/test_login", methods=['POST'])
@jwt_required()
@wrap_request()
def test_login():
    """Test method for logged in user."""
    return {
        'status': "OK",
        'user_id': current_user.id
    }


@bp.route("/get_events", methods=['POST'])
@jwt_required()
@wrap_request()
def test_get_events():
    sleep(1)
    return {'status': "OK"}


@bp.route("/clear_users", methods=['POST'])
@wrap_request()
def clear():
    """Clear all users from db and clear cache."""
    user_count = session.query(UserModel).delete()
    account_count = rpc.account_service.clear()
    return {
        "users removed": user_count,
        "accounts removed": account_count,
    }
