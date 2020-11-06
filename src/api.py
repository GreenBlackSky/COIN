"""Core module contains logic of app."""


from datetime import date
from calendar import monthrange
from temp_mem import Storage, Category


async def add_user(today, initial):
    """Add new user."""
    storage = Storage.get_instance()
    storage.add_user(today, initial)


async def add_event(
    user_uid: int,
    event_date: date,
    value: int,
    category: int,
    comment: str
):
    """Add new event."""
    storage = Storage.get_instance()
    storage.add_event(
        user_uid, event_date,
        value, category, comment
    )


async def set_checkpoint(
        user_uid: int,
        chekpoint_date: date,
        value: int,
        comment: str
):
    """Set new checkpoint."""
    storage = Storage.get_instance()
    current_balance = storage.get_balance(user_uid)
    diff = current_balance - value
    storage.add_event(user_uid, chekpoint_date, diff, Category.Correction, comment)


async def get_balance(user_uid):
    """Get user balance."""
    storage = Storage.get_instance()
    return {"balance": storage.get_balance(user_uid)}


async def get_month(user_uid: int, date_in_month: date):
    """Get list of all events in month."""
    storage = Storage.get_instance()

    # TODO add logic
    # TODO keep local data in redis
    # TODO make use of kubernetes
    # TODO implement ML model
    # TODO make frontend
