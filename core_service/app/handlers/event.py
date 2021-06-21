"""Flask blueprint, that contains events manipulation methods."""

from datetime import datetime

from common.debug_tools import log_function
from common.interfaces import EventService
from common.schemas import EventSchema

from ..model import session, EventModel
from .account import AccountHandler

event_schema = EventSchema()


@log_function
def _event_query(
    account_id,
    after: datetime = None, before: datetime = None,
    with_lables=None, not_with_lables=None
):
    query = session.query(EventModel).filter(
        EventModel.account_id == account_id
    )
    if after:
        query = query.filter(EventModel.event_time > after)
    if before:
        query = query.filter(EventModel.event_time < before)
    # TODO labels
    return query


class EventHandler(EventService):
    """
    Class contains method for handling event stuff.

    Do no instantiate.
    """

    def create_event(
        user_id, account_id, event_time,
        diff, description, confirmed
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
        previous_event = _event_query(account_id, before=event_time).first()

        event = EventModel(
            user_id=user_id,
            account_id=account_id,
            event_time=event_time,
            diff=diff,
            description=description,
            confirmed=confirmed,
        )
        session.add(event)
        session.commit()
        return {'status': 'OK', 'event': event_schema.dump(event)}

    def get_first_event(user_id, account_id, before=None, after=None):
        """
        Get first event by given filters.

        If 0 filters provided, get some event on account.
        """
        if after is not None:
            after = datetime.fromtimestamp(after)
        if before is not None:
            before = datetime.fromtimestamp(before)
        query = _event_query(account_id, after, before)
        if query.filter(EventModel.user_id != user_id).count():
            return {'status': 'accessing another users events'}
        return {
            'status': 'OK',
            'event': event_schema.dump(query.first())
        }

    def get_events(
        user_id, account_id,
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
        query = _event_query(
            account_id, after, before, with_lables, not_with_lables
        )
        if query.filter(EventModel.user_id != user_id).count():
            return {'status': 'accessing another users events'}
        return {
            'status': 'OK',
            'events': [event_schema.dump(event) for event in query.all()]
        }

    def confirm_event(user_id, event_id, confirm):
        """Confirm event."""
        event = session.get(EventModel, event_id)
        if event is None:
            return {'status': 'no such event'}
        if event.user_id != user_id:
            return {'status': 'accessing another users events'}
        event.confirmed = confirm
        session.commit()
        return {'status': 'OK', 'event': event_schema.dump(event)}

    def edit_event(user_id, event_id, event_time, diff, description):
        """Edit existing event."""
        event = session.get(EventModel, event_id)
        if event is None:
            return {'status': 'no such event'}
        if event.user_id != user_id:
            return {'status': 'accessing another users events'}

        event.event_time = datetime.fromtimestamp(event_time)
        event.diff = diff
        event.description = description
        session.commit()
        return {'status': 'OK', 'event': event_schema.dump(event)}

    def delete_event(user_id, event_id):
        """Delete existing event."""
        event = session.get(EventModel, event_id)
        if event is None:
            return {'status': 'no such event'}
        if event.user_id != user_id:
            return {'status': 'accessing another users events'}

        session.delete(event)
        session.commit()
        return {'status': 'OK', 'event': event_schema.dump(event)}

    def clear_events():
        """Clear all events from db."""
        count = session.query(EventModel).delete()
        return count
