"""Flask blueprint, that contains events manipulation methods."""

from celery_abc import CallerMetaBase
from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user

from common.celery_utils import celery_app
from common.debug_tools import log_request
from common.interfaces import EventService

from ..request_helpers import parse_request_args

# BUG events with account_id = null


class EventCaller(EventService, metaclass=CallerMetaBase):
    pass


bp = Blueprint('event_bp', __name__)
eventService = EventCaller(celery_app)


@bp.post("/create_event")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
def create_event(account_id, category_id, event_time, diff, description):
    """Request to create new event."""
    return eventService.create_event(
        current_user.id,
        account_id,
        category_id,
        event_time,
        diff,
        description
    )


@bp.post("/get_events")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
def get_events(
    account_id,
    start_time=None,
    end_time=None,
    category_id=None,
):
    """Get all events user has."""
    return eventService.get_events(
        current_user.id,
        account_id,
        start_time,
        end_time,
        category_id
    )


@bp.post("/edit_event")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
def edit_event(
    account_id,
    event_id,
    category_id,
    event_time,
    diff,
    description
):
    """Request to edit event."""
    return eventService.edit_event(
        current_user.id,
        account_id,
        event_id,
        category_id,
        event_time,
        diff,
        description
    )


@bp.post("/delete_event")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
def delete_event(account_id, event_id):
    """Delete existing event."""
    return eventService.delete_event(current_user.id, account_id, event_id)


@bp.post("/get_balance")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
def get_balance(account_id, category_id, timestamp):
    """Get balance on certain account at certain time."""
    return eventService.get_balance(
        current_user.id,
        account_id,
        category_id,
        timestamp
    )


@bp.post("/get_totals_by_category")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
def get_totals_by_category(
    self,
    account_id,
    category_id,
    start_time,
    end_time
):
    """Get totals on certain account by categories at certain time."""
    return eventService.get_totals_by_category(
        self,
        current_user.id,
        account_id,
        category_id,
        start_time,
        end_time
    )
