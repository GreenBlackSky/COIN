"""Flask blueprint with test methods."""

from time import sleep

from flask import Blueprint, request  # do not remove request just yet
from flask_jwt_extended import jwt_required, current_user

from common.debug_tools import log_request

from ..model import session, UserModel, AccountModel


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


@bp.route("/get_events", methods=['POST'])
@jwt_required()
@log_request
def test_get_events():
    """Mock method for getting events."""
    sleep(1)
    return {'status': "OK"}


@bp.route("/clear_users", methods=['POST'])
@log_request
def clear():
    """Clear all users from db and clear cache."""
    user_count = session.query(UserModel).delete()
    account_count = session.query(AccountModel).delete()
    return {
        "users removed": user_count,
        "accounts removed": account_count,
    }
