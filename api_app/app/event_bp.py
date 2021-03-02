"""Module contains app web."""

import logging
from functools import wraps

from flask import Blueprint, request
from flask_jwt_extended import jwt_required

from . import rpc
from common.debug_tools import log_request


bp = Blueprint('event_bp', __name__)


@bp.route("/create_event", methods=['POST'])
@log_request
@jwt_required()
def create_event():
    """Create new event."""
    pass


@bp.route("/get_event", methods=['POST'])
@log_request
@jwt_required()
def get_event():
    """Get existing event by ID."""


@bp.route("/edit_event", methods=['POST'])
@log_request
@jwt_required()
def edit_event():
    """Edit event."""
    pass


@bp.route("/delete_event", methods=['POST'])
@log_request
@jwt_required()
def delete_event():
    """Get existing event by ID."""
    pass
