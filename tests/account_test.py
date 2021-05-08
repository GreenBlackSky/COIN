"""Accounts stuff tests."""

from datetime import date as dateTools

import requests
from tests.test_base import BaseTest


class AccountTest(BaseTest):
    """Accounts stuff tests."""

    def _unathorized_request(self, request, json_data):
        self.clear_users()
        session = requests.Session()
        self.register(session)
        self.logout(session)
        response = session.post(url=self.HOST+request, json=json_data)
        self.assertEqual(response.status_code, 401, "Wrong response code")
        self.assertDictEqual({}, response.json(), "Got unathorized data")

    def test_get_accounts_unathorized(self):
        """Try get account without authorization."""
        self._unathorized_request('get_accounts', {})

    def test_create_account_unathorized(self):
        """Try get account without authorization."""
        self._unathorized_request('create_account', {'name': 'account2'})

    def test_edit_account_unathorized(self):
        """Try get account without authorization."""
        self._unathorized_request(
            'edit_account', {
                'old_name': 'Main Account',
                'new_name': 'New Account'
            }
        )

    def test_remove_account_unathorized(self):
        """Try get account without authorization."""
        self._unathorized_request('delete_account', {'name': 'Main Account'})

    def test_main_account_created(self):
        """Check if main account was created with user."""
        session = self.prepare(stay_logged_in=True)
        response = session.post(url=self.HOST+"get_accounts",)
        self.assertEqual(response.status_code, 200, "Wrong response code")
        json_data = response.json()
        self.assertDictContainsSubset(
            {'status': 'OK'},
            json_data,
            "Wrong status"
        )
        self.assertIn('accounts', json_data, "No accounts")
        self.assertIsInstance(
            json_data['accounts'],
            list,
            "Wrong accounts type"
        )
        self.assertEqual(len(json_data['accounts']), 1)
        self.assertDictContainsSubset(
            {
                'name': 'Main Account',
                'balance': 0,
                'actual_date': dateTools.today()
            },
            json_data['accounts'][0]
        )

    def test_create_new_account(self):
        raise NotImplementedError()

    def test_create_max_accounts(self):
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
