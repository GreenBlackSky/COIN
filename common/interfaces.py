"""Interfaces of services."""

from .celery_utils import CeleryProxyMetaClass


class AccountService(metaclass=CeleryProxyMetaClass):
    """Account service interface."""

    def create_account(user_id, name):
        """Create new account."""
        pass

    def get_accounts(user_id):
        """Get account from db by id."""
        pass

    def edit_account(user_id, account_id, name):
        """Request to edit account."""
        pass

    def delete_account(user_id, account_id):
        """Delete existing account."""
        pass

    def clear_accounts():
        """Clear all accounts from db and clear cache."""
        pass


class EventService(metaclass=CeleryProxyMetaClass):
    """Event service interface."""

    def create_event(
        user_id, account_id, event_time,
        diff, description, confirmed
    ):
        """Request to create new event."""
        pass

    def get_first_event(user_id, account_id, before, after):
        """Get first event by filter."""
        pass

    def get_events(
        user_id, acc_ids, start_time,
        end_time, with_lables, not_with_lables
    ):
        """Get all events user has."""
        pass

    def confirm_event(user_id, event_id, confirm):
        """Confirm event."""
        pass

    def edit_event(user_id, event_id, event_time, diff, description):
        """Request to edit event."""
        pass

    def delete_event(user_id, event_id):
        """Delete existing event."""
        pass

    def get_balance(user_id, account_id, timestamp):
        """Get balance on account at certain time."""
        pass

    def clear_events():
        """Delete existing event."""
        pass
