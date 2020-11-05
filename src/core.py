"""Core module contains logic of app."""


from datetime import date
from fastapi import FastAPI
from temp_mem import Storage


app = FastAPI()


async def add_user(user_uid: int):
    """Add new user."""
    storage = Storage.get_instance()
    storage.users.add(user_uid)


async def set_checkpoint(
        user_uid: int,
        chekpoint_date: date,
        value: int,
        comment: str
):
    """Set new checkpoint."""
    storage = Storage.get_instance()
    key = (user_uid, chekpoint_date)
    if key in storage.checkpoints:
        return
    storage.checkpoint[key] = (value, comment)


async def add_event(user_uid: int, event_date: date, value: int, comment: str):
    """Add new event."""
    storage = Storage.get_instance()
    key = (user_uid, event_date)
    if key in storage.events:
        return
    storage.checkpoint[key] = (value, comment)


async def get_month(user_uid: int, month: date):
    """Get list of all events in month."""
    pass
