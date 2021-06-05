"""Flask blueprint, that contains events manipulation methods."""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user

from ..request_helpers import parse_request_args
from common.debug_tools import log_request


bp = Blueprint('event_bp', __name__)


@bp.post("/create_event")
@jwt_required()
@parse_request_args(request)
@log_request
def create_event(user_id, acc_id,
                 event_time, diff, total, description, confirmed):
    """Request to create new event."""
    pass


@bp.post("/get_events")
@jwt_required()
@parse_request_args(request)
@log_request
def get_events(acc_ids,
               start_time, end_time,
               with_lables, not_with_lables):
    """Get all events user has."""
    pass


@bp.post("/confirm_event")
@jwt_required()
@parse_request_args(request)
@log_request
def confirm_event(self, event_id):
    """Confirm event."""
    pass


@bp.post("/edit_event")
@jwt_required()
@parse_request_args(request)
@log_request
def edit_event(event_id,
               event_time, diff, total, description):
    """Request to edit event."""
    pass


@bp.post("/delete_event")
@jwt_required()
@parse_request_args(request)
@log_request
def delete_event(event_id):
    """Delete existing event."""
    pass
