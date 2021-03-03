"""Base for most coin of tests."""

import unittest
import requests


class BaseTest(unittest.TestCase):
    """Base test class handles authorization."""

    HOST = "http://localhost:5002/"

    def setUp(self):
        """Set test values."""
        self.user_name = "user1"
        self.user_password = "pass1"

    def register(self, session, name=None, password=None, result=None):
        """Create new account."""
        if name is None:
            name = self.user_name
        if password is None:
            password = self.user_password
        if result is None:
            result = {'status': 'OK'}

        response = session.post(
            url=self.HOST+"register",
            json={'name': name, 'email': name, 'password': password}
        )
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertDictContainsSubset(
            result,
            response.json(),
            "Wrong answear"
        )
        if 'access_token' in response.json():
            session.headers.update(
                {'Authorization': "Bearer " + response.json()['access_token']}
            )
        if 'user' in response.json():
            return response.json()['user']

    def check_authorization(self, session=None, authorized=True):
        """Try access protected resource."""
        if session is None:
            session = requests.Session()
        if authorized:
            result = {'status': "OK"}
            code = 200
        else:
            result = {"status": "unauthorized access"}
            code = 401
        response = session.post(url=self.HOST+"test_login")
        self.assertEqual(response.status_code, code, "Wrong response code")
        self.assertDictContainsSubset(result, response.json(), "Wrong answear")

    def login(self, session, name=None, password=None, result=None):
        """Login."""
        if name is None:
            name = self.user_name
        if password is None:
            password = self.user_password
        if result is None:
            result = {'status': 'OK'}
        response = session.post(
            url=self.HOST+"login",
            json={'email': name, 'password': password}
        )
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertDictContainsSubset(result, response.json(), "Wrong answear")
        if 'access_token' in response.json():
            session.headers.update(
                {'Authorization': "Bearer " + response.json()['access_token']}
            )
        if 'user' in response.json():
            return response.json()['user']

    def logout(self, session):
        """Logout."""
        response = session.post(url=self.HOST+"logout")
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertDictEqual(
            response.json(),
            {'status': 'OK'},
            "Wrong answear"
        )
        if 'Authorization' in session.headers:
            del session.headers['Authorization']

    def clear_users(self):
        """Clear users in app."""
        requests.post(url=self.HOST+"clear_users")
