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
        self._second_user_name = "user2"
        self._second_user_email = "email2"
        self._second_user_password = "pass2"

    def test_unautharized(self):
        """Try unautharized access to app."""
        self.clear_users()
        self.check_authorization(authorized=False)

    def test_login(self):
        """Test logging in."""
        session = self.prepare()
        self.check_authorization(session, authorized=False)
        self.login(session)
        self.check_authorization(session)

    def test_wrong_password(self):
        """Try logging in with wrong password."""
        session = self.prepare()
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
        session = self.prepare()
        self.register(
            session,
            result={'status': 'user already exists'}
        )

    def test_register_while_logged_in(self):
        """Try register user two times in a row."""
        session = self.prepare(stay_logged_in=True)
        self.register(
            session,
            self._second_user_name,
            self._second_user_email,
            self._second_user_password,
            result={'status': 'already authorized'}
        )

    def test_rename_user(self):
        """Test renaming user."""
        session, user = self.prepare(
            stay_logged_in=True,
            get_user=True
        )
        user = self.edit_user('name', self._second_user_name)
        self.logout(session)
        edited_user = self.login(session)
        self.assertDictEqual(user, edited_user)

    def test_change_email(self):
        """Test changing email."""
        session, user = self.prepare(
            stay_logged_in=True,
            get_user=True
        )
        user = self.edit_user(session, email=self._second_user_email)
        self.logout(session)
        edited_user = self.login(session, email=self._second_user_email)
        self.assertDictEqual(user, edited_user)

    def test_change_password(self):
        """Test changing password."""
        session, user = self.prepare(
            stay_logged_in=True,
            get_user=True
        )
        user = self.edit_user('password', self._second_user_password)
        self.logout(session)
        edited_user = self.login(session, password=self._second_user_password)
        self.assertDictEqual(user, edited_user)

    def test_change_password_with_wrong_passwod(self):
        pass
