"""Logging in and co tests."""

import unittest
import requests
from tests.test_base import BaseTest


class LoginTest(BaseTest):
    """Logging in and co tests."""

    def setUp(self):
        """Set test values."""
        BaseTest.setUp(self)
        self._wrong_password = "ass1"
        self._user_email_2 = "email2"
        self._user_password_2 = "pass2"

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
            password=self._wrong_password,
            result={'status': 'wrong password'}
        )
        self.check_authorization(session, authorized=False)

    def test_login_with_wrong_user(self):
        """Test logging in with wrong email."""
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
            self._user_email_2,
            self._user_password_2,
            result={'status': 'already authorized'}
        )

    def test_change_email(self):
        """Test changing email."""
        session, user = self.prepare(
            stay_logged_in=True,
            get_user=True
        )
        response = session.post(
            url=self.HOST+"edit_user",
            json={
                "email": self._user_email_2
            }
        )
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertDictContainsSubset(
            {'status': 'OK'},
            response.json(),
            "Wrong answear"
        )
        self.logout(session)
        user = self.login(session, email=self._user_email_2)
        self.assertEqual(user['email'], self._user_email_2, "Wrong email")

    def test_change_email_into_duplicate(self):
        """Try change email into one, that is already exists."""
        session = self.prepare()
        self.register(session, email=self._user_email_2)
        response = session.post(
            url=self.HOST+"edit_user",
            json={
                "email": self._user_email
            }
        )
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertDictContainsSubset(
            {'status': 'user exists'},
            response.json(),
            "Wrong answear"
        )

    def test_change_password(self):
        """Test changing password."""
        session = self.prepare(stay_logged_in=True)
        response = session.post(
            url=self.HOST+"edit_user",
            json={
                "email": self._user_email,
                "old_pass": self._user_password,
                "new_pass": self._user_password_2
            }
        )
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertDictContainsSubset(
            {'status': 'OK'},
            response.json(),
            "Wrong answear"
        )
        self.logout(session)
        self.login(
            session,
            password=self._user_password,
            result={'status': 'wrong password'}
        )
        self.login(session, password=self._user_password_2)

    def test_change_password_with_wrong_passwod(self):
        """Test changing password with wrong current password."""
        session = self.prepare(stay_logged_in=True)
        response = session.post(
            url=self.HOST+"edit_user",
            json={
                "email": self._user_email,
                "old_pass": self._user_password_2,
                "new_pass": self._user_password
            }
        )
        self.assertEqual(response.status_code, 405, "Wrong response code")
        self.assertDictContainsSubset(
            {'status': 'wrong password'},
            response.json(),
            "Wrong answear"
        )
        self.logout(session)
        self.login(
            session,
            password=self._user_password_2,
            result={"status": "wrong password"}
        )
        self.login(session, password=self._user_password)
