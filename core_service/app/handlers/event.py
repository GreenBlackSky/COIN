"""Flask blueprint, that contains events manipulation methods."""

from datetime import datetime

from celery_abc import WorkerMetaBase
from sqlalchemy import desc
from sqlalchemy.orm.session import Session

from common.celery_utils import celery_app
from common.interfaces import EventService
from common.schemas import EventSchema

from ..model import SavePointModel, session, EventModel
from .account import AccountHandler

event_schema = EventSchema()


def _get_or_create_savepoint(session: Session, account_id, event_time: datetime):
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
        savepoint = SavePointModel(datetime=month_start, account_id=account_id, total=0)
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


def _update_latter_savepoints(session: Session, account_id, event_time: datetime, diff):
    savepoints = (
        session.query(SavePointModel)
        .filter(SavePointModel.account_id == account_id)
        .filter(SavePointModel.datetime >= event_time)
        .all()
    )
    for savepoint in savepoints:
        savepoint.total += diff


class EventHandler(EventService, metaclass=WorkerMetaBase):
    """Class contains method for handling event stuff."""

    def create_event(
        self, user_id, account_id, category_id, event_time, diff, description
    ):
        """Create new event."""
        accounts_response = AccountHandler.check_account_user(account_id, user_id)
        if accounts_response["status"] != "OK":
            return accounts_response

        event_time = datetime.fromtimestamp(event_time)
        event = EventModel(
            user_id=user_id,
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

    def get_first_event(self, user_id, account_id, start_time=None, end_time=None):
        """
        Get first event by given filters.

        If 0 filters provided, get some event on account.
        """
        accounts_response = AccountHandler.check_account_user(account_id, user_id)
        if accounts_response["status"] != "OK":
            return accounts_response

        if start_time is not None:
            start_time = datetime.fromtimestamp(start_time)
        if end_time is not None:
            end_time = datetime.fromtimestamp(end_time)
        query = session.query(EventModel).filter(EventModel.account_id == account_id)
        if start_time:
            query = query.filter(EventModel.event_time > start_time)
        if end_time:
            query = query.filter(EventModel.event_time < end_time)
        return {"status": "OK", "event": event_schema.dump(query.first())}

    def get_events(
        self,
        user_id,
        account_id,
        start_time=None,
        end_time=None,
    ):
        """
        Get all events user has.

        If 0 filters provided, get every event on account.
        """
        accounts_response = AccountHandler.check_account_user(account_id, user_id)
        if accounts_response["status"] != "OK":
            return accounts_response

        if start_time is not None:
            start_time = datetime.fromtimestamp(start_time)
        if end_time is not None:
            end_time = datetime.fromtimestamp(end_time)
        query = session.query(EventModel).filter(EventModel.account_id == account_id)
        if start_time:
            query = query.filter(EventModel.event_time > start_time)
        if end_time:
            query = query.filter(EventModel.event_time < end_time)
        return {
            "status": "OK",
            "events": [event_schema.dump(event) for event in query.all()],
        }

    def edit_event(
        self, user_id, account_id, event_id, category_id, event_time, diff, description
    ):
        """Edit existing event."""
        accounts_response = AccountHandler.check_account_user(account_id, user_id)
        if accounts_response["status"] != "OK":
            return accounts_response

        event = session.get(EventModel, event_id)
        if event is None:
            return {"status": "no such event"}
        if event.user_id != user_id:
            return {"status": "accessing another users events"}
        if event.account_id != account_id:
            return {"status": "wrong account for event"}

        event_time = datetime.fromtimestamp(event_time)
        old_event_time: datetime = event.event_time
        old_diff = event.diff

        event.category_id = category_id
        event.event_time = event_time
        event.diff = diff
        event.description = description

        if old_event_time != event_time:
            _update_latter_savepoints(session, event.account_id, old_event_time, -diff)
            _get_or_create_savepoint(session, event.account_id, event_time)
            _update_latter_savepoints(session, event.account_id, event_time, diff)
        elif old_diff != diff:
            _update_latter_savepoints(
                session, event.account_id, event_time, diff - old_diff
            )
        session.commit()
        return {"status": "OK", "event": event_schema.dump(event)}

    def delete_event(self, user_id, account_id, event_id):
        """Delete existing event."""
        accounts_response = AccountHandler.check_account_user(account_id, user_id)
        if accounts_response["status"] != "OK":
            return accounts_response

        event = session.get(EventModel, event_id)
        if event is None:
            return {"status": "no such event"}
        if event.user_id != user_id:
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

    def get_balance(self, user_id, account_id, timestamp):
        """Get balance on given account in given point in time."""
        accounts_response = AccountHandler.check_account_user(account_id, user_id)
        if accounts_response["status"] != "OK":
            return accounts_response

        timepoint = datetime.fromtimestamp(timestamp)
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

    def get_total_by_category(
        self, user_id, account_id, category_id, start_time, end_time
    ):
        # TODO get_total_by_category
        pass

    def clear_events(self):
        """Clear all events from db."""
        count = session.query(EventModel).delete()
        count = session.query(SavePointModel).delete()
        return count


EventHandler(celery_app)
