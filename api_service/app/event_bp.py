"""Flask blueprint, that contains events manipulation methods."""

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user

from common.debug_tools import wrap_request

from . import rpc


bp = Blueprint('event_bp', __name__)


@bp.post("/create_event")
@jwt_required()
@wrap_request()
def create_event():
    """Request to create new event."""
    return rpc.event_service.create_event()


@bp.post("/get_accounts")
@jwt_required()
@wrap_request()
def get_events():
    """Get all events user has."""
    return rpc.event_service.get_events()


@bp.post("/edit_account")
@jwt_required()
@wrap_request()
def edit_event():
    """Request to edit event."""
    return rpc.event_service.edit_event()


@bp.post("/delete_account")
@jwt_required()
@wrap_request()
def delete_event():
    """Delete existing event."""
    return rpc.event_service.delete_event()
