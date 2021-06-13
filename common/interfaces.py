"""Interfaces of services."""

from .celery_utils import CeleryProxyMetaClass


class AccountService(metaclass=CeleryProxyMetaClass):
    """Account service interface."""

    service_path = "app.handlers.account"

    def create_account(self, user_id, name):
        """Create new account."""
        pass

    def get_accounts(self, user_id):
        """Get account from db by id."""
        pass

    def edit_account(self, user_id, account_id, name):
        """Request to edit account."""
        pass

    def delete_account(self, user_id, account_id):
        """Delete existing account."""
        pass

    def clear_accounts(self):
        """Clear all accounts from db and clear cache."""
        pass


class EventService(metaclass=CeleryProxyMetaClass):
    """Event service interface."""

    service_path = "app.handlers.event"

    def create_event(
        self, user_id, account_id, event_time,
        diff, description, confirmed
    ):
        """Request to create new event."""
        pass

    def get_first_event(self, user_id, account_id, before, after):
        """Get first event by filter."""
        pass

    def get_events(
        self, user_id, acc_ids, start_time,
        end_time, with_lables, not_with_lables
    ):
        """Get all events user has."""
        pass

    def confirm_event(self, user_id, event_id, confirm):
        """Confirm event."""
        pass

    def edit_event(
        self, user_id, event_id, event_time,
        diff, total, description
    ):
        """Request to edit event."""
        pass

    def delete_event(self, user_id, event_id):
        """Delete existing event."""
        pass

    def clear_events(self):
        """Delete existing event."""
        pass
