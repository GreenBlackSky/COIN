"""Accounts stuff tests."""

from datetime import date as dateTools
from typing import Dict, List

import requests
from tests.test_base import BaseTest


class AccountTest(BaseTest):
    """Accounts stuff tests."""

    def _unathorized_request(self, request: str, json_data: Dict[str, str]):
        self.clear_users()
        session = requests.Session()
        self.register(session)
        self.logout(session)
        response = session.post(url=self.HOST+request, json=json_data)
        self.assertEqual(response.status_code, 401, "Wrong response code")
        self.assertDictEqual({}, response.json(), "Got unathorized data")

    def _create_account(
        self, session: requests.Session, account_name: str, result="OK"
    ):
        response = session.post(
            url=self.HOST+"create_account",
            json={'name': account_name}
        )
        self.assertEqual(response.status_code, 200, "Wrong response code")
        json_data = response.json()
        if result == "OK":
            self.assertDictContainsSubset(
                {'status': 'OK'}, json_data, "Wrong response"
            )
            self.assertIn('account', json_data, "No accounts")
            self.assertIsInstance(
                json_data['account'],
                dict,
                "Wrong accounts type"
            )
            self.assertDictContainsSubset(
                {
                    'name': account_name,
                    'balance': 0,
                    'actual_date': dateTools.today()
                },
                json_data['account']
            )
            return json_data['account']
        else:
            self.assertDictEqual(
                json_data,
                {'status': result},
                "Wrong response"
            )

    def _rename_account(
        self, session: requests.Session,
        acc_id: int, name: str,
        result="OK"
    ):
        response = session.post(
            url=self.HOST+"edit_account",
            json={'id': acc_id, 'name': name}
        )
        self.assertEqual(response.status_code, 200, "Wrong response code")
        json_data = response.json()
        if result == "OK":
            self.assertDictContainsSubset(
                {'status': 'OK'}, json_data, "Wrong status or response"
            )
            self.assertIn('account', json_data, "No accounts")
            self.assertIsInstance(
                json_data['account'],
                dict,
                "Wrong accounts type"
            )
            self.assertDictContainsSubset(
                {
                    'id': acc_id,
                    'name': name,
                    'balance': 0,
                    'actual_date': dateTools.today()
                },
                json_data['account']
            )
        else:
            self.assertDictEqual(
                response.json(),
                {'status': result},
                "Wrong response"
            )

    def _delete_account(self, session, acc_id, result="OK"):
        pass

    def _assert_accounts(self, session: requests.Session, accounts: List[str]):
        response = session.post(url=self.HOST+"get_accounts")
        self.assertEqual(response.status_code, 200, "Wrong response code")
        json_data = response.json()
        self.assertIn('accounts', json_data, "No accounts")
        self.assertIsInstance(
            json_data['accounts'],
            list,
            "Wrong accounts type"
        )
        self.assertEqual(
            len(json_data['accounts']),
            len(accounts),
            'Wrong number of accounts'
        )
        response_accounts = {
            account['name']: account
            for account in json_data['accounts']
        }
        for account_name in accounts:
            self.assertIn(account_name, response_accounts, "No such account")
            self.assertDictContainsSubset(
                {
                    'name': account_name,
                    'balance': 0,
                    'actual_date': dateTools.today()
                },
                response_accounts[account_name]
            )

    def test_get_accounts_unathorized(self):
        """Try get account without authorization."""
        raise NotImplementedError()
        self._unathorized_request('get_accounts', {})

    def test_create_account_unathorized(self):
        """Try get account without authorization."""
        raise NotImplementedError()
        self._unathorized_request('create_account', {'name': 'account2'})

    def test_edit_account_unathorized(self):
        """Try get account without authorization."""
        raise NotImplementedError()
        self._unathorized_request(
            'edit_account', {
                'id': 'Main Account',
                'name': 'New Account'
            }
        )

    def test_delete_account_unathorized(self):
        """Try get account without authorization."""
        self.clear_users()
        session = requests.Session()
        self.register(session)
        response = session.post(
            url=self.HOST+'create_account',
            json={'name': 'new account'}
        )
        raise NotImplementedError()
        self.logout(session)
        response = session.post(
            url=self.HOST+'delete_account',
            json={'id': 'new account'}
        )
        self.assertEqual(response.status_code, 401, "Wrong response code")
        self.assertDictEqual({}, response.json(), "Got unathorized data")

    def test_main_account_created(self):
        """Check if main account was created with user."""
        session = self.prepare(stay_logged_in=True)
        self._assert_accounts(session, ["Main Account"])

    def test_create_new_account(self):
        """Test creation of new accounts."""
        session = self.prepare(stay_logged_in=True)
        self._create_account(session, "new account")
        self._assert_accounts(session, ['Main Account', 'new account'])

    def test_create_max_accounts(self):
        """Test create more than maximum number of accounts."""
        session = self.prepare(stay_logged_in=True)
        for i in range(1, 99):
            self._create_account(session, f'account {i}')
        self._assert_accounts(session, [f'account {i}' for i in range(99)])
        self._create_account(session, 'account 100', 'max accounts')

    def test_create_duplicate_account(self):
        """Test creating of account with duplicate."""
        session = self.prepare(stay_logged_in=True)
        self._create_account(session, "new account")
        self._assert_accounts(session, ['Main Account', 'new account'])
        self._create_account(session, "new account", "account already exists")
        self._assert_accounts(session, ['Main Account', 'new account'])

    def test_rename_account(self):
        """Test basic remaning account."""
        session = self.prepare(stay_logged_in=True)
        response = session.post(url=self.HOST+"get_accounts")
        acc_id = response.json()['accounts'][0]
        self._rename_account(session, acc_id, "New account")
        self._assert_accounts(session, ['New account'])

    def test_rename_non_existant_account(self):
        """Test renaming account with wrong id."""
        session = self.prepare(stay_logged_in=True)
        response = session.post(url=self.HOST+"get_accounts")
        acc_id = response.json()['accounts'][0]
        self._rename_account(
            session,
            acc_id + 1,
            "New Account",
            result="no such account"
        )
        self._assert_accounts(session, ['Main Account'])

    def test_rename_account_into_duplicate(self):
        """Test renaming account with name, that is already taken."""
        session = self.prepare(stay_logged_in=True)
        account = self._create_account(session, "new account")
        self._rename_account(
            session,
            account['id'],
            "Main Account",
            result="account already exists"
        )
        self._assert_accounts(session, ["Main Account", "new account"])

    def test_remove_one_account(self):
        session = self.prepare(stay_logged_in=True)
        account = self._create_account(session, "new account")
        response = session.post(
            url=self.HOST+"delete_account",
            json={'id': account['id']}
        )

    def test_remove_non_existant_account(self):
        raise NotImplementedError()

    def test_remove_only_account(self):
        raise NotImplementedError()
