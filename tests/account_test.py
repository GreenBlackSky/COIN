"""Accounts stuff tests."""

from typing import List

from tests.test_base import BaseTest


class AccountTest(BaseTest):
    """Accounts stuff tests."""

    def _create_account(self, account_name: str, result=None, code=200):
        if result is None:
            result = {'status': 'OK'}
        response = self.session.post(
            url=self.HOST+"create_account",
            json={'name': account_name}
        )
        self.assertEqual(response.status_code, code, "Wrong response code")
        json_data = response.json()
        self.assertDictContainsSubset(
            result, json_data, "Wrong response"
        )
        if 'account' in json_data:
            self.assertIsInstance(
                json_data['account'],
                dict,
                "Wrong accounts type"
            )
            self.assertDictContainsSubset(
                {'name': account_name},
                json_data['account']
            )
            return json_data['account']

    def _rename_account(self, account_id, name, result=None, code=200):
        if result is None:
            result = {'status': 'OK'}
        response = self.session.post(
            url=self.HOST+"edit_account",
            json={'id': account_id, 'name': name}
        )
        self.assertEqual(response.status_code, code, "Wrong response code")
        self.assertDictContainsSubset(
            result, response.json(), "Wrong response"
        )

    def _delete_account(self, account_id, result=None, code=200):
        if result is None:
            result = {'status': 'OK'}
        response = self.session.post(
            url=self.HOST+"delete_account",
            json={'id': account_id}
        )
        self.assertEqual(response.status_code, code, "Wrong response code")
        self.assertDictContainsSubset(
            result, response.json(), "Wrong response"
        )

    def _assert_accounts(self, accounts: List[str]):
        response = self.session.post(url=self.HOST+"get_accounts")
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
                {'name': account_name},
                response_accounts[account_name]
            )

    def test_get_accounts_unathorized(self):
        """Try get account without authorization."""
        response = self.session.post(url=self.HOST+"get_accounts")
        self.assertEqual(response.status_code, 401, "Wrong response code")
        self.assertDictEqual(
            {
                'reason': 'Missing Authorization Header',
                'status': 'unauthorized access'
            },
            response.json(),
            "Got unathorized data"
        )

    def test_create_account_unathorized(self):
        """Try get account without authorization."""
        self._create_account(
            'account2',
            code=401,
            result={
                'reason': 'Missing Authorization Header',
                'status': 'unauthorized access'
            },
        )

    def test_edit_account_unathorized(self):
        """Try get account without authorization."""
        self.register()
        account_id = self.get_first_account()['id']
        self.logout()
        self._rename_account(
            account_id,
            'name',
            code=401,
            result={
                'reason': 'Missing Authorization Header',
                'status': 'unauthorized access'
            }
        )

    def test_delete_account_unathorized(self):
        """Try get account without authorization."""
        self.register()
        account_id = self.get_first_account()['id']
        self.logout()
        self._delete_account(
            account_id,
            code=401,
            result={
                'reason': 'Missing Authorization Header',
                'status': 'unauthorized access'
            })

    def test_main_account_created(self):
        """Check if main account was created with user."""
        self.register()
        self._assert_accounts(["Main Account"])

    def test_create_new_account(self):
        """Test creation of new accounts."""
        self.register()
        self._create_account("new account")
        self._assert_accounts(['Main Account', 'new account'])

    def test_create_max_accounts(self):
        """Test create more than maximum number of accounts."""
        self.register()
        for i in range(99):
            self._create_account(f'account {i}')
        self._assert_accounts(
            [f'account {i}' for i in range(99)] + ['Main Account']
        )
        self._create_account('account 100', result={'status': 'max accounts'})

    def test_create_duplicate_account(self):
        """Test creating of account with duplicate."""
        self.register()
        self._create_account("new account")
        self._assert_accounts(['Main Account', 'new account'])
        self._create_account(
            "new account",
            result={'status': "account already exists"}
        )
        self._assert_accounts(['Main Account', 'new account'])

    def test_rename_account(self):
        """Test basic remaning account."""
        self.register()
        account_id = self.get_first_account()['id']
        self._rename_account(account_id, "New account")
        self._assert_accounts(['New account'])

    def test_rename_non_existant_account(self):
        """Test renaming account with wrong id."""
        self.register()
        account_id = self.get_first_account()['id']
        self._rename_account(
            account_id + 1,
            "New Account",
            result={'status': "no such account"}
        )
        self._assert_accounts(['Main Account'])

    def test_rename_account_into_duplicate(self):
        """Test renaming account with name, that is already taken."""
        self.register()
        account = self._create_account("new account")
        self._rename_account(
            account['id'],
            "Main Account",
            result={'status': "account already exists"}
        )
        self._assert_accounts(["Main Account", "new account"])

    def test_remove_one_account(self):
        """Test basic account deleting."""
        self.register()
        account = self._create_account("new account")
        self._delete_account(account['id'])
        self._assert_accounts(["Main Account"])

    def test_remove_non_existant_account(self):
        """Test deleting non-existant account."""
        self.register()
        account = self._create_account("new account")
        self._delete_account(account['id'] + 1, {'status': "no such account"})
        self._assert_accounts(["Main Account", "new account"])

    def test_remove_only_account(self):
        """Test deleting the only account."""
        self.register()
        account_id = self.get_first_account()['id']
        self._delete_account(
            account_id,
            {'status': "can't delete the only account"}
        )
        self._assert_accounts(["Main Account"])

    # def test_create_with_incorrect_args(self):
    #     raise NotImplementedError()

    # def test_edit_with_incorrect_args(self):
    #     raise NotImplementedError()

    # def test_delete_with_incorrect_args(self):
    #     raise NotImplementedError()

    # def test_create_with_too_long_name(self):
    #     raise NotImplementedError()

    # def test_rename_with_too_long_name(self):
    #     raise NotImplementedError()

    # def test_get_account_from_other_user(self):
    #     raise NotImplementedError()

    # def test_rename_account_with_same_name(self):
    #     raise NotImplementedError()
