"""Logging in and co tests."""

import unittest
import requests
from tests.test_base import BaseTest


class LoginTest(BaseTest):
    """Logging in and co tests."""

    def setUp(self):
        """Set test values."""
        BaseTest.setUp(self)
        self._wronguser_password = "ass1"
        self._seconduser_name = "user2"
        self._seconduser_email = "email2"
        self._seconduser_password = "pass2"

    def test_unautharized(self):
        """Try unautharized access to app."""
        self.clear_users()
        self.check_authorization(authorized=False)

    def test_login(self):
        """Test logging in."""
        self.clear_users()
        session = requests.Session()
        self.register(session)
        self.logout(session)
        self.check_authorization(session, authorized=False)
        self.login(session)
        self.check_authorization(session)

    def test_wrong_password(self):
        """Try logging in with wrong password."""
        self.clear_users()
        session = requests.Session()
        self.register(session)
        self.logout(session)
        self.login(
            session,
            password=self._wronguser_password,
            result={'status': 'wrong password'}
        )
        self.check_authorization(session, authorized=False)

    def test_login_with_wrong_user(self):
        """Test logging in with wrong user name."""
        self.clear_users()
        session = requests.Session()
        self.login(session, result={'status': 'no such user'})
        self.check_authorization(session, authorized=False)

    def test_duplicate_register(self):
        """Try register user two times in a row."""
        self.clear_users()
        session = requests.Session()
        self.register(session)
        self.logout(session)
        self.register(
            session,
            result={'status': 'user already exists'}
        )

    def test_register_while_logged_in(self):
        """Try register user two times in a row."""
        self.clear_users()
        session = requests.Session()
        self.register(session)
        self.register(
            session,
            self._seconduser_name,
            self._seconduser_email,
            self._seconduser_password,
            result={'status': 'already authorized'}
        )

    def test_rename_user(self):
        """Try rename user."""
        raise NotImplementedError()

    def test_change_email_user(self):
        """Try rename user."""
        raise NotImplementedError()
