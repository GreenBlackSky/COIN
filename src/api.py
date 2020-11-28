"""Core module contains logic of app."""

from datetime import date
from calendar import monthrange
from flask import Blueprint
from flask_login import login_required


bp = Blueprint('api_bp', __name__)


@bp.route("/add_event", methods=['POST'])
@login_required
def add_event(
    user_uid: str,
    event_date: date,
    value: int,
    category: Category,
    comment: str
):
    """Add new event."""
    storage = Storage.get_instance()
    return {'event_uid': storage.add_event(
        user_uid, event_date,
        value, category, comment
    )}


@bp.route("/correct", methods=['POST'])
@login_required
def correct(
        user_uid: str,
        correction_date: date,
        value: int,
        comment: str
):
    """Correct data."""
    storage = Storage.get_instance()
    current_balance = storage.get_balance(user_uid, correction_date)
    diff = value - current_balance
    return {'event_uid': storage.add_event(
        user_uid,
        correction_date,
        diff,
        Category.Correction,
        comment
    )}


@bp.route("/get_balance", methods=['POST'])
@login_required
def get_balance(user_uid: str, day: date):
    """Get user balance."""
    storage = Storage.get_instance()
    return {"balance": storage.get_balance(user_uid, day)}


@bp.route("/get_month", methods=['POST'])
@login_required
def get_month_data(user_uid: str, month: date):
    """Get list of all events in month."""
    storage = Storage.get_instance()
    return {"month_data": storage.get_month_data(user_uid, month)}
