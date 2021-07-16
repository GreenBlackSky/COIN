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


def _get_or_create_savepoint(
    session: Session,
    account_id,
    event_time: datetime,
    diff
):
    savepoint = session\
        .query(SavePointModel)\
        .filter(SavePointModel.account_id == account_id)\
        .filter(SavePointModel.datetime <= event_time)\
        .order_by(desc(SavePointModel.datetime))\
        .first()

    month_start = event_time.replace(  # month start
        day=1,
        hour=0,
        minute=0,
        second=0,
        microsecond=0
    )
    if savepoint is None:  # earliest savepoint
        savepoint = SavePointModel(
            datetime=month_start,
            total=0
        )
        session.add(savepoint)
    elif savepoint.datetime < month_start:  # new savepoint
        query = session\
            .query(EventModel)\
            .filter(EventModel.account_id == account_id)\
            .filter(EventModel.event_time > savepoint.datetime)\
            .filter(EventModel.event_time < month_start)
        diff_sum = sum(diff for (diff,) in query.values("diff"))
        savepoint = SavePointModel(
            datetime=month_start,
            total=savepoint.total + diff_sum
        )
        session.add(savepoint)


def _update_latter_savepoints(
    session: Session,
    account_id,
    event_time,
    diff
):
    savepoints = session\
        .query(SavePointModel)\
        .filter(SavePointModel.account_id == account_id)\
        .filter(SavePointModel.datetime > event_time)\
        .all()
    for savepoint in savepoints:
        savepoint.totla += diff


class EventHandler(EventService, metaclass=WorkerMetaBase):
    """Class contains method for handling event stuff."""

    def create_event(
        self, user_id, account_id, event_time,
        diff, description  # , confirmed
    ):
        """Create new event."""
        accounts_response = AccountHandler.get_accounts(user_id)
        if accounts_response['status'] != 'OK':
            return accounts_response
        if not any(
            user_acc['id'] == account_id
            for user_acc in accounts_response['accounts']
        ):
            return {'status': 'no such account'}

        event_time = datetime.fromtimestamp(event_time)
        event = EventModel(
            user_id=user_id,
            account_id=account_id,
            event_time=event_time,
            diff=diff,
            description=description,
            # confirmed=confirmed,
        )
        session.add(event)
        _get_or_create_savepoint(
            session,
            account_id,
            event_time,
            diff
        )
        _update_latter_savepoints(session, account_id, event_time, diff)
        session.commit()
        return {'status': 'OK', 'event': event_schema.dump(event)}

    def get_first_event(self, user_id, account_id, before=None, after=None):
        """
        Get first event by given filters.

        If 0 filters provided, get some event on account.
        """
        if after is not None:
            after = datetime.fromtimestamp(after)
        if before is not None:
            before = datetime.fromtimestamp(before)
        query = session\
            .query(EventModel)\
            .filter(EventModel.account_id == account_id)
        if after:
            query = query.filter(EventModel.event_time > after)
        if before:
            query = query.filter(EventModel.event_time < before)
        return {
            'status': 'OK',
            'event': event_schema.dump(query.first())
        }

    def get_events(
        self, user_id, account_id,
        after=None, before=None,
        with_lables=None, not_with_lables=None
    ):
        """
        Get all events user has.

        If 0 filters provided, get every event on account.
        """
        if after is not None:
            after = datetime.fromtimestamp(after)
        if before is not None:
            before = datetime.fromtimestamp(before)
        # TODO labels
        query = session\
            .query(EventModel)\
            .filter(EventModel.account_id == account_id)
        if after:
            query = query.filter(EventModel.event_time > after)
        if before:
            query = query.filter(EventModel.event_time < before)
        return {
            'status': 'OK',
            'events': [event_schema.dump(event) for event in query.all()]
        }

    # def confirm_event(user_id, event_id, confirm):
    #     """Confirm event."""
    #     event = session.get(EventModel, event_id)
    #     if event is None:
    #         return {'status': 'no such event'}
    #     if event.user_id != user_id:
    #         return {'status': 'accessing another users events'}
    #     event.confirmed = confirm
    #     session.commit()
    #     return {'status': 'OK', 'event': event_schema.dump(event)}

    def edit_event(self, user_id, event_id, event_time, diff, description):
        """Edit existing event."""
        event = session.get(EventModel, event_id)
        if event is None:
            return {'status': 'no such event'}
        if event.user_id != user_id:
            return {'status': 'accessing another users events'}
        event_time = datetime.fromtimestamp(event_time)
        event.event_time = event_time
        event.diff = diff
        event.description = description
        _get_or_create_savepoint(
            session,
            event.account_id,
            event_time,
            diff
        )
        _update_latter_savepoints(
            session,
            event.account_id,
            event_time,
            diff
        )
        session.commit()
        return {'status': 'OK', 'event': event_schema.dump(event)}

    def delete_event(self, user_id, event_id):
        """Delete existing event."""
        event = session.get(EventModel, event_id)
        if event is None:
            return {'status': 'no such event'}
        if event.user_id != user_id:
            return {'status': 'accessing another users events'}

        session.delete(event)
        # TODO remove savepoint if event is a last one
        _update_latter_savepoints(
            session,
            event.account_id,
            event.event_time,
            -event.diff
        )
        session.commit()
        return {'status': 'OK', 'event': event_schema.dump(event)}

    def get_balance(self, user_id, account_id, timestamp):
        """Get balance on given account in given point in time."""
        timepoint = datetime.fromtimestamp(timestamp)
        savepoint = session\
            .query(SavePointModel)\
            .filter(SavePointModel.account_id == account_id)\
            .filter(SavePointModel.datetime <= timepoint)\
            .order_by(desc(SavePointModel.datetime))\
            .first()

        if savepoint is None:
            return {'status': 'OK', 'balance': 0}

        query = session\
            .query(EventModel)\
            .filter(EventModel.account_id == account_id)\
            .filter(EventModel.event_time > savepoint.datetime)\
            .filter(EventModel.event_time < timepoint)
        diff_sum = sum(diff for (diff,) in query.values("diff"))
        return {'status': 'OK', 'balance': savepoint.total + diff_sum}

    def clear_events(self):
        """Clear all events from db."""
        count = session.query(EventModel).delete()
        return count


EventHandler(celery_app)
