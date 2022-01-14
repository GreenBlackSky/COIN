"""Base for most coin of tests."""

import unittest
import requests


class BaseTest(unittest.TestCase):
    """Base test class handles authorization."""

    HOST = "http://localhost:5004/"

    def setUp(self):
        """Set test values."""
        self.user_password = "pass1"
        self.user_name = "name1"
        requests.post(url=self.HOST + "clear_users")
        self.session = requests.Session()

    def register(self, name=None, password=None, result=None):
        """Create new account."""
        if password is None:
            password = self.user_password
        if name is None:
            name = self.user_name
        if result is None:
            result = {"status": "OK"}

        response = self.session.post(
            url=self.HOST + "register", json={"name": name, "password": password}
        )
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertDictContainsSubset(result, response.json(), "Wrong answear")
        if "access_token" in response.json():
            self.session.headers.update(
                {"Authorization": "Bearer " + response.json()["access_token"]}
            )
        return response.json().get("user")

    def check_authorization(self, authorized=True):
        """Try access protected resource."""
        if self.session is None:
            self.session = requests.Session()
        if authorized:
            result = {"status": "OK"}
            code = 200
        else:
            result = {"status": "unauthorized access"}
            code = 401
        response = self.session.post(url=self.HOST + "test_login")
        self.assertEqual(response.status_code, code, "Wrong response code")
        self.assertDictContainsSubset(result, response.json(), "Wrong answear")

    def login(self, name=None, password=None, result=None, code=200):
        """Login."""
        if name is None:
            name = self.user_name
        if password is None:
            password = self.user_password
        if result is None:
            result = {"status": "OK"}
        response = self.session.post(
            url=self.HOST + "login", json={"name": name, "password": password}
        )
        self.assertEqual(response.status_code, code, "Wrong response code")
        self.assertDictContainsSubset(result, response.json(), "Wrong answear")
        if "access_token" in response.json():
            self.session.headers.update(
                {"Authorization": "Bearer " + response.json()["access_token"]}
            )
        if "user" in response.json():
            return response.json()["user"]

    def logout(self):
        """Logout."""
        response = self.session.post(url=self.HOST + "logout")
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertDictEqual(response.json(), {"status": "OK"}, "Wrong answear")
        if "Authorization" in self.session.headers:
            del self.session.headers["Authorization"]

    def get_first_account(self):
        response = self.session.post(url=self.HOST + "get_accounts")
        self.assertEqual(response.status_code, 200, "Wrong response code")
        json_data = response.json()
        self.assertIn("accounts", json_data, "No accounts")
        self.assertIsInstance(json_data["accounts"], list, "Wrong accounts type")
        self.assertNotEqual(len(json_data["accounts"]), 0, "No accounts")
        account = response.json()["accounts"][0]
        self.assertIsInstance(account, dict, "Account is not dict")
        self.assertIn("name", account, "No name in account")
        self.assertIn("id", account, "No id in account")
        return account
