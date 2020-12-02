"""Cache app api."""

import logging


def get_user_data():
    """Get user data."""
    pass


def get_unaccepted():
    """Get all events that are already happend, but were not accepted."""
    pass


def accept_event():
    """Accept unaccepted event."""
    pass


def get_day_events():
    """Get events in one day."""
    pass


def get_month():
    """Get statistics for month."""
    pass


def get_year():
    """Get statistics for year."""
    pass


def get_all_years():
    """Get info on all user history."""
    pass


def add_event():
    return {"method": "add_event"}


def edit_event():
    return {"method": "edit_event"}


def get_templates():
    return {"method": "get_templates"}


def add_template():
    return {"method": "add_template"}


def edit_template():
    return {"method": "edit_template"}


def get_statistics():
    return {"method": "get_statistics"}
