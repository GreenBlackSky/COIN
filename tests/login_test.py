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
        response = session.post(
            url=self.HOST+"edit_user",
            json={
                "username": self._second_user_name,
                "email": self._user_email
            }
        )
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertDictContainsSubset(
            {'status': 'OK'},
            response.json(),
            "Wrong answear"
        )
        self.logout(session)
        user = self.login(session)
        self.assertEqual(user['name'], self._second_user_name, "Wrong name")

    def test_change_email(self):
        """Test changing email."""
        session, user = self.prepare(
            stay_logged_in=True,
            get_user=True
        )
        response = session.post(
            url=self.HOST+"edit_user",
            json={
                "username": self._user_name,
                "email": self._second_user_email
            }
        )
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertDictContainsSubset(
            {'status': 'OK'},
            response.json(),
            "Wrong answear"
        )
        self.logout(session)
        user = self.login(session, email=self._second_user_email)
        self.assertEqual(user['email'], self._second_user_email, "Wrong email")

    def test_change_email_into_duplicate(self):
        """Try change email into one, that is already exists."""
        session, user1 = self.prepare(
            stay_logged_in=True,
            get_user=True
        )
        self.logout(session)
        user2 = self.register(session, email=self._second_user_email)
        response = session.post(
            url=self.HOST+"edit_user",
            json={
                "username": self._user_name,
                "email": self._user_email
            }
        )
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertDictContainsSubset(
            {'status': 'user already exists'},
            response.json(),
            "Wrong answear"
        )

    def test_change_password(self):
        """Test changing password."""
        session, user = self.prepare(
            stay_logged_in=True,
            get_user=True
        )
        response = session.post(
            url=self.HOST+"edit_user",
            json={
                "username": self._user_name,
                "email": self._user_email,
                "old_pass": self._user_password,
                "new_pass": self._second_user_password
            }
        )
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertDictContainsSubset(
            {'status': 'OK'},
            response.json(),
            "Wrong answear"
        )
        self.logout(session)
        self.login(session, password=self._second_user_password)

    def test_change_password_with_wrong_passwod(self):
        """Test changing password with wrong current password."""
        session, user = self.prepare(
            stay_logged_in=True,
            get_user=True
        )
        response = session.post(
            url=self.HOST+"edit_user",
            json={
                "username": self._user_name,
                "email": self._user_email,
                "old_pass": self._second_user_password,
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
            password=self._second_user_password,
            result={"status": "wrong password"}
        )
        self.login(session, password=self._user_password)
