"""Module contains app web."""

import logging
from functools import wraps

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from . import rpc
from common.debug_tools import log_request


bp = Blueprint('api_bp', __name__)


@bp.route("/get_account", methods=['POST'])
@log_request
@jwt_required()
def get_account():
    """Get existing account by ID."""
    request_data = request.get_json()
    if request_data is None:
        return {'status': 'no json data'}
    account_id = request_data.get('account_id')
    if account_id is None:
        return {'status': 'incomplete user data'}
    account = rpc.cache_service.get_account(account_id)
    return {
        'status': 'OK',
        'account': account
    }


@bp.route("/rename_account", methods=['POST'])
@log_request
@jwt_required()
def rename_account():
    """Get existing account by ID."""
    pass


@bp.route("/set_main_account", methods=['POST'])
@log_request
@jwt_required()
def set_main_account():
    """Get existing account by ID."""
    pass


@bp.route("/delete_account", methods=['POST'])
@log_request
@jwt_required()
def delete_account():
    """Get existing account by ID."""
    pass


# @bp.route("/add_event", methods=['POST'])
# @jwt_required()
# def add_event():
#     """Add new event."""
#     return {"method": "add_event"}


# @bp.route("/get_unaccepted", methods=['POST'])
# @login_required
# def get_unaccepted():
#     """Get all events that are already happend, but were not accepted."""
#     pass


# @bp.route("/accept_event", methods=['POST'])
# @login_required
# def accept_event():
#     """Accept unaccepted event."""
#     pass


# @bp.route("/get_day", methods=['POST'])
# @login_required
# def get_day_events():
#     """Get events in one day."""
#     pass


# @bp.route("/edit_event", methods=['POST'])
# @login_required
# def edit_event():
#     """Edit event."""
#     return {"method": "edit_event"}


# @bp.route("/get_templates", methods=['POST'])
# @login_required
# def get_templates():
#     """Get event templates."""
#     return {"method": "get_templates"}


# @bp.route("/add_template", methods=['POST'])
# @login_required
# def add_template():
#     """Add new event template."""
#     return {"method": "add_template"}


# @bp.route("/edit_template", methods=['POST'])
# @login_required
# def edit_template():
#     """Edit event template."""
#     return {"method": "edit_template"}


# @bp.route("/get_statistics", methods=['POST'])
# @login_required
# def get_statistics():
#     """Get statistic data."""
#     return {"method": "get_statistics"}
