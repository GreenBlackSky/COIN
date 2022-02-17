"""Flask blueprint, that contains events manipulation methods."""

import datetime as dt

from flask import Blueprint, request
from flask_jwt_extended import jwt_required, current_user
from sqlalchemy import desc
from sqlalchemy.orm.session import Session

from .account_bp import check_account
from .debug_tools import log_request
from .model import session, EventModel, SavePointModel
from .request_helpers import parse_request_args
from .schemas import EventSchema

# BUG events with account_id = null


bp = Blueprint("event_bp", __name__)
event_schema = EventSchema()


def _get_or_create_savepoint(
    session: Session, account_id, event_time: dt.datetime
):
    # event in the start of the month is not accounted for
    # in the savepoint at a same time, it would be in a next savepoint
    savepoint = (
        session.query(SavePointModel)
        .filter(SavePointModel.account_id == account_id)
        .filter(SavePointModel.datetime < event_time)
        .order_by(desc(SavePointModel.datetime))
        .first()
    )

    month_start = event_time.replace(  # month start
        day=1, hour=0, minute=0, second=0, microsecond=0
    )
    if savepoint is None:  # earliest savepoint
        savepoint = SavePointModel(
            datetime=month_start, account_id=account_id, total=0
        )
        session.add(savepoint)
    elif savepoint.datetime < month_start:  # new savepoint
        query = (
            session.query(EventModel)
            .filter(EventModel.account_id == account_id)
            .filter(EventModel.event_time >= savepoint.datetime)
            .filter(EventModel.event_time < month_start)
            .with_entities(EventModel.diff)
        )
        diff_sum = sum(diff for (diff,) in query)
        savepoint = SavePointModel(
            datetime=month_start, total=savepoint.total + diff_sum
        )
        session.add(savepoint)


def _update_latter_savepoints(
    session: Session, account_id, event_time: dt.datetime, diff
):
    savepoints = (
        session.query(SavePointModel)
        .filter(SavePointModel.account_id == account_id)
        .filter(SavePointModel.datetime >= event_time)
        .all()
    )
    for savepoint in savepoints:
        savepoint.total += diff


@bp.post("/create_event")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
@check_account
def create_event(account_id, category_id, event_time, diff, description):
    """Request to create new event."""
    event_time = dt.datetime.fromtimestamp(event_time)
    event = EventModel(
        user_id=current_user.id,
        account_id=account_id,
        category_id=category_id,
        event_time=event_time,
        diff=diff,
        description=description,
    )
    session.add(event)
    _get_or_create_savepoint(session, account_id, event_time)
    _update_latter_savepoints(session, account_id, event_time, diff)
    session.commit()
    return {"status": "OK", "event": event_schema.dump(event)}


@bp.post("/get_events")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
@check_account
def get_events(account_id, start_time=None, end_time=None):
    """Get all events user has."""
    if start_time is not None:
        start_time = dt.datetime.fromtimestamp(start_time)
    if end_time is not None:
        end_time = dt.datetime.fromtimestamp(end_time)
    query = session.query(EventModel).filter(
        EventModel.account_id == account_id
    )
    if start_time:
        query = query.filter(EventModel.event_time > start_time)
    if end_time:
        query = query.filter(EventModel.event_time < end_time)
    return {
        "status": "OK",
        "events": [event_schema.dump(event) for event in query.all()],
    }


@bp.post("/edit_event")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
@check_account
def edit_event(
    account_id, event_id, category_id, event_time, diff, description
):
    """Request to edit event."""
    event = session.get(EventModel, event_id)
    if event is None:
        return {"status": "no such event"}
    if event.user_id != current_user.id:
        return {"status": "accessing another users events"}
    if event.account_id != account_id:
        return {"status": "wrong account for event"}

    event_time = dt.datetime.fromtimestamp(event_time)
    old_event_time: dt.datetime = event.event_time
    old_diff = event.diff

    event.category_id = category_id
    event.event_time = event_time
    event.diff = diff
    event.description = description

    if old_event_time != event_time:
        _update_latter_savepoints(
            session, event.account_id, old_event_time, -diff
        )
        _get_or_create_savepoint(session, event.account_id, event_time)
        _update_latter_savepoints(session, event.account_id, event_time, diff)
    elif old_diff != diff:
        _update_latter_savepoints(
            session, event.account_id, event_time, diff - old_diff
        )
    session.commit()
    return {"status": "OK", "event": event_schema.dump(event)}


@bp.post("/delete_event")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
@check_account
def delete_event(account_id, event_id):
    """Delete existing event."""
    event = session.get(EventModel, event_id)
    if event is None:
        return {"status": "no such event"}
    if event.user_id != current_user.id:
        return {"status": "accessing another users events"}
    if event.account_id != account_id:
        return {"status": "wrong account for event"}

    session.delete(event)
    # TODO remove savepoint if event is a last one
    _update_latter_savepoints(
        session, event.account_id, event.event_time, -event.diff
    )
    session.commit()
    return {"status": "OK", "event": event_schema.dump(event)}


@bp.post("/get_balance")
@jwt_required()
@log_request(request, current_user)
@parse_request_args(request)
@check_account
def get_balance(account_id, timestamp):
    """Get balance on certain account at certain time."""
    timepoint = dt.datetime.fromtimestamp(timestamp)
    savepoint = (
        session.query(SavePointModel)
        .filter(SavePointModel.account_id == account_id)
        .filter(SavePointModel.datetime <= timepoint)
        .order_by(desc(SavePointModel.datetime))
        .first()
    )

    if savepoint is None:
        return {"status": "OK", "balance": 0}

    diff_sum = sum(
        event.diff
        for event in session.query(EventModel.diff)
        .filter(EventModel.account_id == account_id)
        .filter(EventModel.event_time >= savepoint.datetime)
        .filter(EventModel.event_time < timepoint)
        .all()
    )
    return {"status": "OK", "balance": savepoint.total + diff_sum}


def get_category_total(account_id, category_id, start_time, end_time):
    """
    Get total income for given time in given category.

    start_time and end_time are both datetime.
    """
    return sum(
        event.diff
        for event in session.query(EventModel.diff)
        .filter(EventModel.account_id == account_id)
        .filter(EventModel.category_id == category_id)
        .filter(EventModel.event_time >= start_time)
        .filter(EventModel.event_time < end_time)
        .all()
    )


def delete_events_by_category(account_id, category_id):
    """Delete all events in one category."""
    session.execute(
        EventModel.delete()
        .where(EventModel.account_id == account_id)
        .where(EventModel.category_id == category_id)
    )


def move_events_between_categories(account_id, category_from, category_to):
    """Move all events from one category to another."""
    session.execute(
        EventModel.update()
        .values(category_id=category_to)
        .where(EventModel.account_id == account_id)
        .where(EventModel.category_id == category_from)
    )
