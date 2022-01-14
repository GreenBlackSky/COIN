"""Flask blueprint with test methods."""

from time import sleep

from celery_abc import CallerMetaBase
from flask import Blueprint, request  # do not remove request just yet
from flask_jwt_extended import jwt_required, current_user

from common.celery_utils import celery_app
from common.debug_tools import log_request
from common.interfaces import AccountService, EventService

from ..model import session, UserModel


class AccountCaller(AccountService, metaclass=CallerMetaBase):
    pass


class EventCaller(EventService, metaclass=CallerMetaBase):
    pass


bp = Blueprint("test_bp", __name__)
accountService = AccountCaller(celery_app)
eventService = EventCaller(celery_app)


@bp.route("/test_login", methods=["POST"])
@jwt_required()
@log_request(request, current_user)
def test_login():
    """Test method for logged in user."""
    return {"status": "OK", "user_id": current_user.id}


@bp.route("/clear_users", methods=["POST"])
@log_request(request, current_user)
def clear():
    """Clear all users from db and clear cache."""
    events_count = eventService.clear_events()
    account_count = accountService.clear_accounts()
    user_count = session.query(UserModel).delete()
    return {
        "events removed": events_count,
        "accounts removed": account_count,
        "users removed": user_count,
    }
