"""Flask blueprint, that contains events manipulation methods."""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user

from common.debug_tools import log_request
from common.interfaces import EventService

from ..request_helpers import parse_request_args

bp = Blueprint('event_bp', __name__)


@bp.post("/create_event")
@jwt_required()
@log_request(request)
def create_event():
    """Request to create new event."""
    args = (
        'user_id', 'acc_id', 'event_time', 'diff',
        'total', 'description', 'confirmed'
    )
    vals, _ = parse_request_args(request, args)
    return EventService.create_event(
        **{key: val for key, val in zip(args, vals)}
    )


@bp.post("/get_events")
@jwt_required()
@log_request(request)
def get_events():
    """Get all events user has."""
    args = (
        'acc_ids', 'start_time', 'end_time',
        'with_lables', 'not_with_lables'
    )
    vals, _ = parse_request_args(request, args)
    return EventService.get_events(
        **{key: val for key, val in zip(args, vals)}
    )


@bp.post("/confirm_event")
@jwt_required()
@log_request(request)
def confirm_event():
    """Confirm event."""
    args = ('event_id',)
    vals, _ = parse_request_args(request, args)
    return EventService.confirm_event(
        **{key: val for key, val in zip(args, vals)}
    )


@bp.post("/edit_event")
@jwt_required()
@log_request(request)
def edit_event():
    """Request to edit event."""
    args = ('event_id', 'event_time', 'diff', 'total', 'description')
    vals, _ = parse_request_args(request, args)
    return EventService.edit_event(
        **{key: val for key, val in zip(args, vals)}
    )


@bp.post("/delete_event")
@jwt_required()
@log_request(request)
def delete_event():
    """Delete existing event."""
    args = ('event_id',)
    vals, _ = parse_request_args(request, args)
    return EventService.delete_event(
        **{key: val for key, val in zip(args, vals)}
    )
