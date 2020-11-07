"""Core module contains logic of app."""
# TODO async
# TODO FastApi
# TODO make use of kubernetes
# TODO implement ML model
# TODO make frontend

from datetime import date
from calendar import monthrange
from core import Storage, Category


def add_user(today, initial):
    """Add new user."""
    storage = Storage.get_instance()
    return storage.add_user(today, initial)


def add_event(
    user_uid: str,
    event_date: date,
    value: int,
    category: Category,
    comment: str
):
    """Add new event."""
    storage = Storage.get_instance()
    storage.add_event(
        user_uid, event_date,
        value, category, comment
    )


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
    storage.add_event(user_uid, correction_date, diff, Category.Correction, comment)


def get_balance(user_uid: str, day: date):
    """Get user balance."""
    storage = Storage.get_instance()
    return {"balance": storage.get_balance(user_uid, day)}


def get_month_data(user_uid: str, month: date):
    """Get list of all events in month."""
    storage = Storage.get_instance()
    return {"month_data": storage.get_month_data(user_uid, month)}
