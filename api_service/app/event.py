"""FastAPI blueprint, that contains events manipulation methods."""

import datetime as dt

from fastapi import APIRouter, Depends
from pydantic import BaseModel
from sqlalchemy import desc, select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import sessionmaker

from .exceptions import LogicException
from .models import (
    UserModel,
    EventModel,
    SavePointModel,
    create_account_entry,
)
from .user import authorized_user
from .database import get_session


router = APIRouter()


async def _update_or_create_savepoint(
    session: AsyncSession, user_id, account_id, event_time: dt.datetime
):
    # event in the start of the month is not accounted for
    # in the savepoint at a same time, it would be in a next savepoint
    month_start = event_time.replace(
        day=1, hour=0, minute=0, second=0, microsecond=0
    )
    query = (
        await session.execute(
            select(SavePointModel)
            .where(SavePointModel.user_id == user_id)
            .where(SavePointModel.account_id == account_id)
            .where(SavePointModel.datetime < event_time)
            .order_by(desc(SavePointModel.datetime))
        )
    ).first()

    if not query:  # earliest savepoint
        savepoint = await create_account_entry(
            session,
            SavePointModel,
            user_id=user_id,
            account_id=account_id,
            datetime=month_start,
            total=0,
        )
        session.add(savepoint)
    elif query[0].datetime < month_start:  # new savepoint
        query = await session.execute(
            select(EventModel.diff)
            .where(EventModel.user_id == user_id)
            .where(EventModel.account_id == account_id)
            .where(EventModel.event_time >= savepoint.datetime)
            .where(EventModel.event_time < month_start)
        )

        savepoint = await create_account_entry(
            session,
            SavePointModel,
            user_id=user_id,
            account_id=account_id,
            datetime=month_start,
            total=savepoint.total + sum(diff for (diff,) in query.all()),
        )
        session.add(savepoint)


async def _update_latter_savepoints(
    session: AsyncSession, user_id, account_id, event_time: dt.datetime, diff
):
    savepoints = (
        await session.execute(
            select(SavePointModel)
            .where(SavePointModel.user_id == user_id)
            .where(SavePointModel.account_id == account_id)
            .where(SavePointModel.datetime >= event_time)
        )
    ).all()
    for (savepoint,) in savepoints:
        savepoint.total += diff


class EventData(BaseModel):
    account_id: int
    category_id: int
    event_time: int
    diff: int
    description: str


@router.post("/create_event")
async def create_event(
    event_data: EventData,
    current_user: UserModel = Depends(authorized_user),
    async_session: sessionmaker = Depends(get_session),
):
    """Request to create new event."""
    event_time = dt.datetime.fromtimestamp(event_data.event_time)
    session: AsyncSession
    async with async_session() as session:
        event: EventModel = await create_account_entry(
            session,
            EventModel,
            user_id=current_user.id,
            account_id=event_data.account_id,
            category_id=event_data.category_id,
            event_time=event_time,
            diff=event_data.diff,
            description=event_data.description,
        )
        session.add(event)
        await _update_or_create_savepoint(
            session, current_user.id, event_data.account_id, event_time
        )
        await _update_latter_savepoints(
            session,
            current_user.id,
            event_data.account_id,
            event_time,
            event_data.diff,
        )
        await session.commit()
    return {"status": "OK", "event": event.to_dict()}


class GetEventsRequest(BaseModel):
    account_id: int
    start_time: int | None = None
    end_time: int | None = None


@router.post("/get_events")
async def get_events(
    request: GetEventsRequest,
    current_user: UserModel = Depends(authorized_user),
    async_session: sessionmaker = Depends(get_session),
):
    """Get all events user has."""
    query = (
        select(EventModel)
        .where(EventModel.user_id == current_user.id)
        .where(EventModel.account_id == request.account_id)
    )
    if request.start_time:
        query = query.where(
            EventModel.event_time
            > dt.datetime.fromtimestamp(request.start_time)
        )
    if request.end_time:
        query = query.where(
            EventModel.event_time < dt.datetime.fromtimestamp(request.end_time)
        )
    session: AsyncSession
    async with async_session() as session:
        events = await session.execute(query)
        return {
            "status": "OK",
            "events": [event.to_dict() for (event,) in events.all()],
        }


class EditEventRequest(BaseModel):
    event_id: int
    account_id: int
    category_id: int
    event_time: int
    diff: int
    description: str


@router.post("/edit_event")
async def edit_event(
    request: EditEventRequest,
    current_user: UserModel = Depends(authorized_user),
    async_session: sessionmaker = Depends(get_session),
):
    """Request to edit event."""
    session: AsyncSession
    async with async_session() as session:
        event: EventModel = await session.get(
            EventModel,
            (current_user.id, request.account_id, request.event_id),
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
            await _update_latter_savepoints(
                session,
                current_user.id,
                event.account_id,
                old_event_time,
                -request.diff,
            )
            await _update_or_create_savepoint(
                session, current_user.id, event.account_id, event_time
            )
            await _update_latter_savepoints(
                session,
                current_user.id,
                event.account_id,
                event_time,
                request.diff,
            )
        elif old_diff != request.diff:
            await _update_latter_savepoints(
                session,
                current_user.id,
                event.account_id,
                event_time,
                request.diff - old_diff,
            )
        await session.commit()

    return {"status": "OK", "event": event.to_dict()}


class DeleteEventRequest(BaseModel):
    account_id: int
    event_id: int


@router.post("/delete_event")
async def delete_event(
    request: DeleteEventRequest,
    current_user: UserModel = Depends(authorized_user),
    async_session: sessionmaker = Depends(get_session),
):
    """Delete existing event."""
    session: AsyncSession
    async with async_session() as session:
        async with session.begin():
            event: EventModel = await session.get(
                EventModel,
                (current_user.id, request.account_id, request.event_id),
            )
            if event is None:
                raise LogicException("no such event")

            await session.delete(event)
            # TODO remove savepoint if event is a last one
            await _update_latter_savepoints(
                session,
                current_user.id,
                event.account_id,
                event.event_time,
                -event.diff,
            )

    return {"status": "OK", "event": event.to_dict()}


class GetBalanceRequest(BaseModel):
    account_id: int
    timestamp: int


@router.post("/get_balance")
async def get_balance(
    request: GetBalanceRequest,
    current_user: UserModel = Depends(authorized_user),
    async_session: sessionmaker = Depends(get_session),
):
    """Get balance on certain account at certain time."""
    timepoint = dt.datetime.fromtimestamp(request.timestamp)

    session: AsyncSession
    async with async_session() as session:
        query = (
            await session.execute(
                select(SavePointModel)
                .where(SavePointModel.user_id == current_user.id)
                .where(SavePointModel.account_id == request.account_id)
                .where(SavePointModel.datetime <= timepoint)
                .order_by(desc(SavePointModel.datetime))
            )
        ).first()

        print("!", query)

        if not query:
            return {"status": "OK", "balance": 0}

        (savepoint,) = query
        query = await session.execute(
            select(EventModel.diff)
            .where(EventModel.user_id == current_user.id)
            .where(EventModel.account_id == request.account_id)
            .where(EventModel.event_time >= savepoint.datetime)
            .where(EventModel.event_time < timepoint)
        )
    return {
        "status": "OK",
        "balance": savepoint.total + sum(diff for (diff,) in query.all()),
    }


async def get_category_total(
    session: AsyncSession, account_id, category_id, start_time, end_time
):
    """
    Get total income for given time in given category.

    start_time and end_time are both datetime.
    """
    query = await session.execute(
        select(EventModel.diff)
        .where(EventModel.account_id == account_id)
        .where(EventModel.category_id == category_id)
        .where(EventModel.event_time >= start_time)
        .where(EventModel.event_time < end_time)
    )
    return sum(diff for (diff,) in query.all())
