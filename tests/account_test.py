"""Accounts stuff tests."""

import requests
from tests.test_base import BaseTest


class AccountTest(BaseTest):
    """Accounts stuff tests."""

    def test_get_accounts(self):
        raise NotImplementedError()

    def test_get_accounts_unathorized(self):
        """Try get account without authorization."""
        self.clear_users()
        session = requests.Session()
        user_data = self.register(session)
        self.logout(session)
        raise NotImplementedError()

    def test_create_account_unathorized(self):
        """Try get account without authorization."""
        raise NotImplementedError()

    def test_edit_account_unathorized(self):
        """Try get account without authorization."""
        raise NotImplementedError()

    def test_remove_account_unathorized(self):
        """Try get account without authorization."""
        raise NotImplementedError()

    def test_main_account_created(self):
        """Check if main account was created with user."""
        raise NotImplementedError()

    def test_create_new_account(self):
        raise NotImplementedError()

    def test_create_duplicate_account(self):
        raise NotImplementedError()

    def test_rename_account(self):
        raise NotImplementedError()

    def test_rename_non_existant_account(self):
        raise NotImplementedError()

    def test_rename_account_into_duplicate(self):
        raise NotImplementedError()

    def test_remove_one_account(self):
        raise NotImplementedError()

    def test_remove_non_existant_account(self):
        raise NotImplementedError()

    def test_remove_only_account(self):
        raise NotImplementedError()
