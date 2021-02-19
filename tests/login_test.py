"""Logging in and co test."""

import unittest
import requests


class Login(unittest.TestCase):
    """Class for coin tests."""

    HOST = "http://localhost:5002/"

    def setUp(self):
        """Set test values."""
        self._user_name = "user1"
        self._user_password = "pass1"
        self._wrong_user_password = "ass1"
        self._second_user_name = "user2"
        self._second_user_password = "pass2"

    def _register(self, session, name, password, result=None):
        if result is None:
            result = {'status': 'OK'}

        response = session.post(
            url=self.HOST+"register",
            json={'name': name, 'password': password}
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

    def _try(self, session=None, authorized=True):
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

    def _login(self, session, name=None, password=None, result=None):
        if name is None:
            name = self._user_name
        if password is None:
            password = self._user_password
        if result is None:
            result = {'status': 'OK'}
        response = session.post(
            url=self.HOST+"login",
            json={'name': name, 'password': password}
        )
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertDictContainsSubset(result, response.json(), "Wrong answear")
        if 'access_token' in response.json():
            session.headers.update(
                {'Authorization': "Bearer " + response.json()['access_token']}
            )

    def _logout(self, session):
        response = session.post(url=self.HOST+"logout")
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertDictEqual(
            response.json(),
            {'status': 'OK'},
            "Wrong answear"
        )
        if 'Authorization' in session.headers:
            del session.headers['Authorization']

    def test_unautharized(self):
        """Try unautharized access to app."""
        requests.post(url=self.HOST+"clear_users")
        self._try(authorized=False)

    def test_register(self):
        """Test regestring new user."""
        requests.post(url=self.HOST+"clear_users")
        session = requests.Session()
        self._register(session, self._user_name, self._user_password)
        self._try(session)

    def test_logout(self):
        """Test logging out."""
        requests.post(url=self.HOST+"clear_users")
        session = requests.Session()
        self._register(session, self._user_name, self._user_password)
        self._logout(session)
        self._try(session, authorized=False)

    def test_login(self):
        """Test logging in."""
        requests.post(url=self.HOST+"clear_users")
        session = requests.Session()
        self._register(session, self._user_name, self._user_password)
        self._logout(session)
        self._try(session, authorized=False)
        self._login(session)
        self._try(session)

    def test_wrong_password(self):
        """Try logging in with wrong password."""
        requests.post(url=self.HOST+"clear_users")
        session = requests.Session()
        self._register(session, self._user_name, self._user_password)
        self._logout(session)
        self._login(
            session,
            password=self._wrong_user_password,
            result={'status': 'wrong password'}
        )
        self._try(session, authorized=False)

    def test_login_with_wrong_user(self):
        """Test logging in with wrong user name."""
        requests.post(url=self.HOST+"clear_users")
        session = requests.Session()
        self._login(session, result={'status': 'no such user'})
        self._try(session, authorized=False)

    def test_duplicate_register(self):
        """Try register user two times in a row."""
        requests.post(url=self.HOST+"clear_users")
        session = requests.Session()
        self._register(session, self._user_name, self._user_password)
        self._logout(session)
        self._register(
            session,
            self._user_name,
            self._user_password,
            result={'status': 'user already exists'}
        )

    def test_register_while_logged_in(self):
        """Try register user two times in a row."""
        requests.post(url=self.HOST+"clear_users")
        session = requests.Session()
        self._register(session, self._user_name, self._user_password)
        self._register(
            session,
            self._second_user_name,
            self._second_user_password,
            result={'status': 'already authorized'}
        )
