"""
Savepoint.

Util methods that works with savepoints -
data structire, that keeps data on balance
on certain account in certain point in time.

Lets say, we create one savepoint at the start of each month,
that has some events in it.
"""

from datetime import datetime

from sqlalchemy.orm import Session

from ..model import SavePointModel


def _get_closest_savepoint(session: Session, account_id, timestamp):
    """Get closest savepoint, that is earlier than given time."""
    return session\
        .query(SavePointModel)\
        .filter(SavePointModel.account_id == account_id)\
        .filter(SavePointModel.save_point_date <= timestamp)\
        .first()


def get_closest_savepoint(session: Session, account_id, timestamp):
    """
    Get balance and time of the closest savepoint,
    that is earlier than given time.
    """
    savepoint = _get_closest_savepoint(session, account_id, timestamp)
    return savepoint.balance, savepoint.savepoint_time


def ensure_savepoint(session: Session, account_id, timestamp):
    """
    If there id no savepoint in the start of current month, create one.

    Get time of the savepoint at the start of the month.
    """
    savepoint = _get_closest_savepoint(session, account_id, timestamp)
    month_start = datetime\
        .fromtimestamp(timestamp)\
        .replace(day=0, hour=0, minute=0, second=0, microsecond=0)\
        .timestamp()
    if savepoint is None or savepoint.save_point_date < month_start:
        new_savepoint = SavePointModel(
            save_point_date=month_start,
            total=0
        )
        session.add(new_savepoint)
    return month_start


def clear_savepoints(session, account_id):
    pass
