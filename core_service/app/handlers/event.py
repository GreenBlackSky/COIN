"""Flask blueprint, that contains events manipulation methods."""

from datetime import datetime

from common.celery_utils import celery_app
from common.debug_tools import log_function, log_method
from common.schemas import EventSchema

from ..model import session, EventModel
from .account import get_accounts

event_schema = EventSchema()


@log_function
def _event_query(
    account_id,
    after=None, before=None,
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


@celery_app.task
@log_function
def create_event(
    user_id, account_id, event_time,
    diff, description, confirmed
):
    """Create new event."""
    accounts_response = get_accounts(user_id)
    if accounts_response['status'] != 'OK':
        return accounts_response
    if not any(
        user_acc['id'] == account_id
        for user_acc in accounts_response['accounts']
    ):
        return {'status': 'no such account'}

    event_time = datetime.fromtimestamp(event_time)
    previous_event = _event_query(account_id, before=event_time).first()
    if previous_event is None:
        total = 0
    else:
        total = previous_event['total'] + diff

    event = EventModel(
        user_id=user_id,
        account_id=account_id,
        event_time=event_time,
        diff=diff,
        total=total,
        description=description,
        confirmed=confirmed,
    )
    session.add(event)
    session.commit()
    return {'status': 'OK', 'event': event_schema.dump(event)}


@celery_app.task
@log_function
def get_first_event(user_id, account_id, after, before):
    """
    Get first event by given filters.

    If 0 filters provided, get some event on account.
    """
    after = datetime.fromtimestamp(after)
    before = datetime.fromtimestamp(before)
    query = _event_query(account_id, after, before)
    if query.filter(EventModel.user_id != user_id).count():
        return {'status': 'accessing another users events'}
    return {
        'status': 'OK',
        'events': [event_schema.dump(event) for event in query.first()]
    }


@celery_app.task
@log_function
def get_events(
    user_id, account_id,
    after, before,
    with_lables, not_with_lables
):
    """
    Get all events user has.

    If 0 filters provided, get every event on account.
    """
    after = datetime.fromtimestamp(after)
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


@celery_app.task
@log_function
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


@celery_app.task
@log_function
def edit_event(
    user_id, event_id, event_time,
    diff, total, description
):
    """Edit existing event."""
    event = session.get(EventModel, event_id)
    if event is None:
        return {'status': 'no such event'}
    if event.user_id != user_id:
        return {'status': 'accessing another users events'}

    event.event_time = datetime.fromtimestamp(event_time)
    event.diff = diff
    event.total = total
    event.description = description
    session.commit()
    return {'status': 'OK', 'event': event_schema.dump(event)}


@celery_app.task
@log_function
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


@celery_app.task
@log_function
def clear_events():
    """Clear all events from db."""
    count = session.query(EventModel).delete()
    return count
