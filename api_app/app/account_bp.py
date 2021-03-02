"""Module contains app web."""

import logging
from functools import wraps

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from . import rpc
from common.debug_tools import log_request


bp = Blueprint('account_bp', __name__)


@bp.route("/create_account", methods=['POST'])
@log_request
@jwt_required()
def create_account():
    """Create new account."""
    pass


@bp.route("/get_account", methods=['POST'])
@log_request
@jwt_required()
def get_account():
    """Get existing account by ID."""


@bp.route("/edit_account", methods=['POST'])
@log_request
@jwt_required()
def edit_account():
    """Edit account."""
    pass


@bp.route("/delete_account", methods=['POST'])
@log_request
@jwt_required()
def delete_account():
    """Get existing account by ID."""
    pass
