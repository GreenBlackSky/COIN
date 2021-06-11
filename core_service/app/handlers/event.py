"""Flask blueprint, that contains events manipulation methods."""

from common.celery_utils import celery_app
from common.debug_tools import log_method
from common.schemas import EventSchema

from ..model import session, EventModel


event_schema = EventSchema()


@celery_app.task
@log_method
def create_event(
    user_id, acc_id, event_time,
    diff, total, description
):
    """Create new event."""
    event = EventModel(
        user_id=user_id,
        acc_id=acc_id,
        event_time=event_time,
        diff=diff,
        total=total,
        description=description,
        confirmed=False,
    )
    session.add(event)
    session.commit()
    return {'status': 'OK', 'account': event_schema.dump(event)}


@celery_app.task
@log_method
def get_events(user_id, acc_ids, after, before, with_lables, not_with_lables):
    """Get all events user has."""
    query = session.query(EventModel).filter(
        EventModel.acc_id.in_(acc_ids)
    )
    if query.filter(EventModel.user_id != user_id).count():
        return {'status': 'accessing another users events'}
    if after:
        query = query.filter(EventModel.event_time > after)
    if before:
        query = query.filter(EventModel.event_time < before)
    # TODO labels
    return {
        'status': 'OK',
        'events': [event_schema.dump(event) for event in query.all()]
    }


@celery_app.task
@log_method
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
@log_method
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

    event.event_time = event_time
    event.diff = diff
    event.total = total
    event.description = description
    session.commit()
    return {'status': 'OK', 'event': event_schema.dump(event)}


@celery_app.task
@log_method
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
@log_method
def clear_events():
    """Clear all events from db."""
    count = session.query(EventModel).delete()
    return count
