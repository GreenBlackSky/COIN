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
        'acc_id', 'event_time', 'diff',
        'total', 'description'
    )
    vals, _ = parse_request_args(request, args)
    kvals = {key: val for key, val in zip(args, vals)}
    kvals['acc_ids'] = current_user.id
    return EventService.create_event(**kvals)


@bp.post("/get_events")
@jwt_required()
@log_request(request)
def get_events():
    """Get all events user has."""
    (acc_ids,), kvals = parse_request_args(
        request,
        ('acc_ids',),
        ('start_time', 'end_time', 'with_lables', 'not_with_lables')
    )
    kvals['acc_ids'] = acc_ids
    kvals['user_id'] = current_user.id
    return EventService.get_events(**kvals)


@bp.post("/confirm_event")
@jwt_required()
@log_request(request)
def confirm_event():
    """Confirm event."""
    (event_id, confirm), _ = parse_request_args(
        request, ('event_id', 'confirm')
    )
    return EventService.confirm_event(
        user_id=current_user.id,
        event_id=event_id,
        confirm=confirm
    )


@bp.post("/edit_event")
@jwt_required()
@log_request(request)
def edit_event():
    """Request to edit event."""
    args = ('event_id', 'event_time', 'diff', 'total', 'description')
    vals, _ = parse_request_args(request, args)
    kvals = {key: val for key, val in zip(args, vals)}
    kvals['user_id'] = current_user.id
    return EventService.edit_event(**kvals)


@bp.post("/delete_event")
@jwt_required()
@log_request(request)
def delete_event():
    """Delete existing event."""
    args = ('event_id',)
    (event_id,), _ = parse_request_args(request, args)
    return EventService.delete_event(
        user_id=current_user.id,
        event_id=event_id,
    )
