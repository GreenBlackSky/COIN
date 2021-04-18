"""Accounts stuff tests."""

import requests
from tests.test_base import BaseTest


class AccountTest(BaseTest):
    """Accounts stuff tests."""

    def _try_get_account(self, session, account_id, authorized=True):
        if authorized:
            result = {'status': "OK"}
            code = 200
        else:
            result = {"status": "unauthorized access"}
            code = 401
        response = session.post(
            url=self.HOST+"get_account",
            json={'account_id': account_id}
        )
        self.assertEqual(response.status_code, code, "Wrong response code")
        self.assertDictContainsSubset(
            result,
            response.json(),
            "Wrong answear"
        )

    def test_get_unathorized(self):
        """Try get account without authorization."""
        self.clear_users()
        session = requests.Session()
        user_data = self.register(session)
        self.logout(session)
        self._try_get_account(session, user_data['accounts'][0], False)

    def test_main_account_created(self):
        """Check if main account was created with user."""
        self.clear_users()
        session = requests.Session()
        user_data = self.register(session)
        self._try_get_account(session, user_data['accounts'][0], False)

    def test_create_new_account(self):
        self.clear_users()
        session = requests.Session()
        user_data = self.register(session)

    def test_rename_account(self):
        raise NotImplementedError()

    def test_remove_one_account(self):
        raise NotImplementedError()

    def test_remove_only_account(self):
        raise NotImplementedError()
