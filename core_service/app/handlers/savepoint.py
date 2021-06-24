"""
Savepoint.

Util methods that works with savepoints -
data structire, that keeps data on balance
on certain account in certain point in time.
"""


def save_change(session, account_id, timestamp, change):
    pass


def get_closest_savepoint(session, account_id, timestamp):
    pass


def clear_savepoints(session, account_id):
    pass


def _create_savepoint(session, account_id, timestamp, total):
    pass


def _get_savepoint(session, account_id, before=None, after=None):
    pass


def _edit_savepoint(session, savepoint_id, diff):
    pass


def _delete_savepoint(session, account_id, timestamp):
    pass
