"""Core module contains logic of app."""
# TODO connect to db
# TODO caching into redis

from datetime import datetime, timedelta
import logging
from typing import List
from collections import defaultdict
from flask import Blueprint, request
from flask_login import login_required, current_user
from dateutil.relativedelta import relativedelta
from .models import db, User, Category, Event, Template


bp = Blueprint('api_bp', __name__)


def _process_time_marker(time_marker, zero_fields, user_id):
    if time_marker is None:
        logging.error(f"{user_id} no time_marker ")
        return

    try:
        day = datetime.fromtimestamp(day)
    except Exception as e:
        logging.error(f"{user_id} invalid time_marker {time_marker}")
        return

    logging.debug(f"{user_id} time_marker {time_marker}")

    return day.replace(**{field: 0 for field in zero_fields})


@bp.route("/get_user_data", methods=('POST',))
@login_required
def get_user_data():
    """Get user data."""
    name = current_user.name
    user = User.query.filter_by(name=name).first()
    logging.debug(f"{current_user.id} get_user_data {name}")
    return user.serialize()


@bp.route("/accept_event", methods=('POST',))
@login_required
def accept_event():
    """Accept unaccepted event."""
    event_id = request.args.get('event_id')
    if event_id is None:
        logging.error(f"{current_user.id} accept_event no event_id in request")
        return

    event = Event.query.filter(Event.id == event_id).first()
    if event is None:
        logging.error(f"{current_user.id} accept_event no event {event_id}")
        return
    if event.accepted:
        logging.error(f"{current_user.id} accept_event event {event_id} is already accepted")
        return

    event.accepted = True
    db.session.commit()
    logging.debug(f"{current_user.id} accept_event event {event_id} accepted")


@bp.route("/get_day", methods=('POST',))
@login_required
def get_day_events():
    """Get events in one day."""
    day = _process_time_marker(
        request.args.get('day'),
        ('hour', 'minute', 'second', 'microsecond'),
        current_user.id
    )
    if day is None:
        return

    start = day
    end = day + timedelta(days=1)

    events = Event.query.filter(
        Event.user_id == current_user.id,
        Event.date >= start,
        Event.date <= end
    ).all()

    events = [event.serialize for event in events]
    logging.debug(f"{current_user.id} get_day_events {day} {events}")
    return events


@bp.route("/get_month", methods=('POST',))
@login_required
def get_month():
    """Get statistics for month."""
    month = _process_time_marker(
        request.args.get('month'),
        ('day', 'hour', 'minute', 'second', 'microsecond'),
        current_user.id
    )
    if month is None:
        return

    start = month
    end = month + relativedelta(months=+1)

    events: List[Event] = Event.query.filter(
        Event.user_id == current_user.id,
        Event.date >= start,
        Event.date <= end
    ).all()

    days = defaultdict(lambda: 0)
    for event in events:
        days[event.date.day] += event.value
    logging.debug(f"{current_user.id} get_month {month} {days}")
    return dict(days)


@bp.route("/get_year", methods=('POST',))
@login_required
def get_year():
    """Get statistics for year."""
    year = _process_time_marker(
        request.args.get('month'),
        ('month', 'day', 'hour', 'minute', 'second', 'microsecond'),
        current_user.id
    )
    if year is None:
        return

    start = year
    end = year + relativedelta(years=+1)

    events: List[Event] = Event.query.filter(
        Event.user_id == current_user.id,
        Event.date >= start,
        Event.date <= end
    ).all()

    months = defaultdict(lambda: 0)
    for event in events:
        months[event.date.month] += event.value
    logging.debug(f"{current_user.id} get_year {year} {months}")
    return dict(months)


@bp.route("/get_all_years", methods=('POST',))
@login_required
def get_all_years():
    return {"method": "get_all_years"}


@bp.route("/add_event", methods=('POST',))
@login_required
def add_event():
    return {"method": "add_event"}


@bp.route("/edit_event", methods=('POST',))
@login_required
def edit_event():
    return {"method": "edit_event"}


@bp.route("/get_templates", methods=('POST',))
@login_required
def get_templates():
    return {"method": "get_templates"}


@bp.route("/add_template", methods=('POST',))
@login_required
def add_template():
    return {"method": "add_template"}


@bp.route("/edit_template", methods=('POST',))
@login_required
def edit_template():
    return {"method": "edit_template"}


@bp.route("/get_statistics", methods=('POST',))
@login_required
def get_statistics():
    return {"method": "get_statistics"}
