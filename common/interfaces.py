"""Interfaces of services."""

from .celery_utils import CeleryProxyMetaClass


class AccountService(metaclass=CeleryProxyMetaClass):
    """Account service interface."""

    service_path = "app.handlers.account"

    def create_account(user_id, name):
        """Create new account."""
        pass

    def get_accounts(user_id):
        """Get account from db by id."""
        pass

    def edit_account(user_id, acc_id, name):
        """Request to edit account."""
        pass

    def delete_account(user_id, acc_id):
        """Delete existing account."""
        pass

    def clear_accounts():
        """Clear all accounts from db and clear cache."""
        pass
