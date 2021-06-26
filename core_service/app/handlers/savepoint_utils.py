"""
Savepoint.

Util methods that works with savepoints -
data structire, that keeps data on balance
on certain account in certain point in time.

Lets say, we create one savepoint at the start of each month,
that has some events in it.
"""

from datetime import datetime

from sqlalchemy import desc
from sqlalchemy.orm import Session

from ..model import SavePointModel


# TODO remove
def get_closest_savepoint(session: Session, account_id, before: datetime):
    """Get closest savepoint, that is earlier than given time."""
    return session\
        .query(SavePointModel)\
        .filter(SavePointModel.account_id == account_id)\
        .filter(SavePointModel.datetime <= before)\
        .order_by(desc(SavePointModel.datetime))\
        .first()
