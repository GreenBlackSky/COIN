"""Flask blueprint, that contains events manipulation methods."""

import datetime as dt

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import desc
from sqlalchemy.orm.session import Session

from .exceptions import LogicException
from .model import (
    UserModel,
    session,
    EventModel,
    SavePointModel,
    EventSchema,
    create_account_entry,
)
from .user import authorized_user


router = APIRouter()


def _dump_event(event: EventModel):
    schema = EventSchema.from_orm(event)
    dump = schema.dict()
    dump["event_time"] = schema.event_time.timestamp()
    return dump


def _get_or_create_savepoint(
    session: Session, user_id, account_id, event_time: dt.datetime
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
        savepoint = create_account_entry(
            SavePointModel,
            user_id=user_id,
            account_id=account_id,
            datetime=month_start,
            total=0,
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


class EventData(BaseModel):
    account_id: int
    category_id: int
    event_time: int
    diff: int
    description: str


@router.post("/create_event")
def create_event(
    event_data: EventData, current_user: UserModel = Depends(authorized_user)
):
    """Request to create new event."""
    event_time = dt.datetime.fromtimestamp(event_data.event_time)
    event = create_account_entry(
        EventModel,
        user_id=current_user.id,
        account_id=event_data.account_id,
        category_id=event_data.category_id,
        event_time=event_time,
        diff=event_data.diff,
        description=event_data.description,
    )
    session.add(event)
    _get_or_create_savepoint(
        session, current_user.id, event_data.account_id, event_time
    )
    _update_latter_savepoints(
        session, event_data.account_id, event_time, event_data.diff
    )
    session.commit()
    return {"status": "OK", "event": _dump_event(event)}


class GetEventsRequest(BaseModel):
    account_id: int
    start_time: int | None = None
    end_time: int | None = None


@router.post("/get_events")
def get_events(
    request: GetEventsRequest,
    current_user: UserModel = Depends(authorized_user),
):
    """Get all events user has."""
    query = (
        session.query(EventModel)
        .filter(EventModel.user_id == current_user.id)
        .filter(EventModel.account_id == request.account_id)
    )
    if request.start_time:
        query = query.filter(
            EventModel.event_time
            > dt.datetime.fromtimestamp(request.start_time)
        )
    if request.end_time:
        query = query.filter(
            EventModel.event_time < dt.datetime.fromtimestamp(request.end_time)
        )
    return {
        "status": "OK",
        "events": [_dump_event(event) for event in query.all()],
    }


class EditEventRequest(BaseModel):
    event_id: int
    account_id: int
    category_id: int
    event_time: int
    diff: int
    description: str


@router.post("/edit_event")
def edit_event(
    request: EditEventRequest,
    current_user: UserModel = Depends(authorized_user),
):
    """Request to edit event."""
    event = session.query(EventModel).get(
        (current_user.id, request.account_id, request.event_id)
    )
    if event is None:
        raise LogicException("no such event")

    event_time = dt.datetime.fromtimestamp(request.event_time)
    old_event_time: dt.datetime = event.event_time
    old_diff = event.diff

    event.category_id = request.category_id
    event.event_time = event_time
    event.diff = request.diff
    event.description = request.description

    if old_event_time != event_time:
        _update_latter_savepoints(
            session, event.account_id, old_event_time, -request.diff
        )
        _get_or_create_savepoint(
            session, current_user.id, event.account_id, event_time
        )
        _update_latter_savepoints(
            session, event.account_id, event_time, request.diff
        )
    elif old_diff != request.diff:
        _update_latter_savepoints(
            session, event.account_id, event_time, request.diff - old_diff
        )
    session.commit()
    return {"status": "OK", "event": _dump_event(event)}


class DeleteEventRequest(BaseModel):
    account_id: int
    event_id: int


@router.post("/delete_event")
def delete_event(
    request: DeleteEventRequest,
    current_user: UserModel = Depends(authorized_user),
):
    """Delete existing event."""
    event = session.query(EventModel).get(
        (current_user.id, request.account_id, request.event_id)
    )
    if event is None:
        raise LogicException("no such event")

    session.delete(event)
    # TODO remove savepoint if event is a last one
    _update_latter_savepoints(
        session, event.account_id, event.event_time, -event.diff
    )
    session.commit()
    return {"status": "OK", "event": _dump_event(event)}


class GetBalanceRequest(BaseModel):
    account_id: int
    timestamp: int


@router.post("/get_balance")
def get_balance(
    request: GetBalanceRequest,
    current_user: UserModel = Depends(authorized_user),
):
    """Get balance on certain account at certain time."""
    timepoint = dt.datetime.fromtimestamp(request.timestamp)
    savepoint = (
        session.query(SavePointModel)
        .filter(SavePointModel.account_id == request.account_id)
        .filter(SavePointModel.datetime <= timepoint)
        .order_by(desc(SavePointModel.datetime))
        .first()
    )

    if savepoint is None:
        return {"status": "OK", "balance": 0}

    diff_sum = sum(
        event.diff
        for event in session.query(EventModel.diff)
        .filter(EventModel.account_id == request.account_id)
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


def delete_events_by_category(user_id, account_id, category_id):
    """Delete all events in one category."""
    (
        session.query(EventModel)
        .filter(EventModel.user_id == user_id)
        .filter(EventModel.account_id == account_id)
        .filter(EventModel.category_id == category_id)
        .delete()
    )
    session.commit()


def move_events_between_categories(
    user_id, account_id, category_id, category_to
):
    """Move all events from one category to another."""
    (
        session.query(EventModel)
        .filter(EventModel.user_id == user_id)
        .filter(EventModel.account_id == account_id)
        .filter(EventModel.category_id == category_id)
        .update({EventModel.category_id: category_to})
    )
    session.commit()
