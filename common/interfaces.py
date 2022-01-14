"""Interfaces of services."""

from abc import ABC, abstractmethod


class AccountService(ABC):
    """Account service interface."""

    @abstractmethod
    def create_account(self, user_id, name):
        """Create new account."""
        pass

    @abstractmethod
    def get_accounts(self, user_id):
        """Get account from db by id."""
        pass

    @abstractmethod
    def edit_account(self, user_id, account_id, name):
        """Request to edit account."""
        pass

    @abstractmethod
    def delete_account(self, user_id, account_id):
        """Delete existing account."""
        pass

    @abstractmethod
    def clear_accounts(self):
        """Clear all accounts from db and clear cache."""
        pass


class EventService(ABC):
    """Event service interface."""

    @abstractmethod
    def create_event(
        self, user_id, account_id, category_id, event_time, diff, description
    ):
        """Request to create new event."""
        pass

    @abstractmethod
    def get_first_event(self, user_id, account_id, start_time, end_time):
        """Get first event by filter."""
        pass

    @abstractmethod
    def get_events(self, user_id, account_id, start_time=None, end_time=None):
        """Get all events user has."""
        pass

    # def confirm_event(user_id, event_id, confirm):
    #     """Confirm event."""
    #     pass

    # TODO make unchanged parametres optional
    @abstractmethod
    def edit_event(
        self, user_id, account_id, event_id, category_id, event_time, diff, description
    ):
        """Request to edit event."""
        pass

    @abstractmethod
    def delete_event(self, user_id, account_id, event_id):
        """Delete existing event."""
        pass

    @abstractmethod
    def get_balance(self, user_id, account_id, timestamp):
        """Get balance on account at certain time."""
        pass

    @abstractmethod
    def clear_events(self):
        """Delete existing event."""
        pass


class CategoryService(ABC):
    """Event category service interface."""

    @abstractmethod
    def create_category(self, user_id, account_id, name, color):
        """Request to create new events category."""
        pass

    @abstractmethod
    def get_categories(self, user_id, account_id):
        """Get all categories user has."""
        pass

    @abstractmethod
    def edit_category(self, user_id, account_id, category_id, name, color):
        """Request to edit events category."""
        pass

    @abstractmethod
    def delete_category(self, user_id, account_id, category_id):
        """Delete existing events category."""
        pass
