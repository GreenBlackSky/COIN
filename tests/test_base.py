"""Base for most coin of tests."""

import unittest
import requests


class BaseTest(unittest.TestCase):
    """Base test class handles authorization."""

    HOST = "http://localhost:5002/"

    def setUp(self):
        """Set test values."""
        self._user_name = "user1"
        self._user_password = "pass1"
        self._user_email = "email1"

    def prepare(self, stay_logged_in=False, get_user=False):
        """Clesr users and create new one."""
        self.clear_users()
        session = requests.Session()
        user = self.register(session)
        if not stay_logged_in:
            self.logout(session)
        if get_user:
            return session, user
        return session

    def register(self, session, name=None, email=None, password=None, result=None):
        """Create new account."""
        if name is None:
            name = self._user_name
        if password is None:
            password = self._user_password
        if email is None:
            email = self._user_email
        if result is None:
            result = {'status': 'OK'}

        response = session.post(
            url=self.HOST+"register",
            json={'name': name, 'email': email, 'password': password}
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

    def login(self, session, email=None, password=None, result=None):
        """Login."""
        if email is None:
            email = self._user_email
        if password is None:
            password = self._user_password
        if result is None:
            result = {'status': 'OK'}
        response = session.post(
            url=self.HOST+"login",
            json={'email': email, 'password': password}
        )
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertDictContainsSubset(result, response.json(), "Wrong answear")
        if 'access_token' in response.json():
            session.headers.update(
                {'Authorization': "Bearer " + response.json()['access_token']}
            )
        if 'user' in response.json():
            return response.json()['user']

    def edit_user(self, session, user, field_name, value):
        """Test edit user."""
        user[field_name] = self._seconduser_name
        response = session.post(
            url=self.HOST+"edit_user",
            json={field_name, value}
        )
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertDictContainsSubset(
            {'status': 'OK'},
            response.json(),
            "Wrong answear"
        )
        return user

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
