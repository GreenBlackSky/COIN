"""
Savepoint - data structire, that keeps data on balance
on certain account in certain point in time.
"""


def create_savepoint(session, account_id, timestamp, total):
    pass


def get_savepoint(session, account_id, before=None, after=None):
    pass


def edit_savepoint(session, savepoint_id, diff):
    pass


def delete_savepoint(session, account_id, timestamp):
    pass
