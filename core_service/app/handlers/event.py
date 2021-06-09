"""Flask blueprint, that contains events manipulation methods."""

from common.debug_tools import log_method


@log_method
def create_event(
    user_id, acc_id, event_time,
    diff, total, description, confirmed
):
    """Request to create new event."""
    pass


@log_method
def get_events(
    user_id, acc_ids, start_time,
    end_time, with_lables, not_with_lables
):
    """Get all events user has."""
    pass


@log_method
def confirm_event(user_id, event_id):
    """Confirm event."""
    pass


@log_method
def edit_event(
    user_id, event_id, event_time,
    diff, total, description
):
    """Request to edit event."""
    pass


@log_method
def delete_event(user_id, event_id):
    """Delete existing event."""
    pass
