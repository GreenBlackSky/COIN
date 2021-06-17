"""Logging in and co tests."""

from tests.test_base import BaseTest


class LoginTest(BaseTest):
    """Logging in and co tests."""

    def _edit_user(self, name,
                   old_pass=None, new_pass=None, result=None, code=200):
        user_data = {'name': name}
        if old_pass and new_pass:
            user_data.update({
                'old_pass': old_pass,
                'new_pass': new_pass
            })
        if result is None:
            result = {'status': 'OK'}
        response = self.session.post(
            url=self.HOST+"edit_user",
            json=user_data
        )
        self.assertEqual(response.status_code, code, "Wrong response code")
        self.assertDictContainsSubset(
            result,
            response.json(),
            "Wrong answear"
        )

    def setUp(self):
        """Set test values."""
        BaseTest.setUp(self)
        self.wrong_password = "ass1"
        self.user_name_2 = "name2"
        self.user_password_2 = "pass2"

    def test_unautharized(self):
        """Try unautharized access to app."""
        self.check_authorization(authorized=False)

    def test_login_and_logout(self):
        """Test logging in."""
        self.register()
        self.check_authorization()
        self.logout()
        self.check_authorization(authorized=False)
        self.login()
        self.check_authorization()

    def test_wrong_password(self):
        """Try logging in with wrong password."""
        self.register()
        self.logout()
        self.login(
            password=self.wrong_password,
            result={'status': 'wrong password'},
            code=401
        )
        self.check_authorization(authorized=False)

    def test_login_with_wrong_user(self):
        """Test logging in with wrong name."""
        self.register()
        self.logout()
        self.login(
            self.user_name_2,
            code=401,
            result={'status': 'no such user'},
        )
        self.check_authorization(authorized=False)

    def test_duplicate_register(self):
        """Try register user two times in a row."""
        self.register()
        self.logout()
        self.register(result={'status': 'user exists'})

    def test_register_while_logged_in(self):
        """Try register user two times in a row."""
        self.register()
        self.register(
            self.user_name_2,
            self.user_password_2,
            result={'status': 'already authorized'}
        )

    def test_change_name_unauthorized(self):
        """Try editing unser data without authorization."""
        self.register()
        self.logout()
        self._edit_user(
            self.user_name_2,
            code=401,
            result={
                'reason': 'Missing Authorization Header',
                'status': 'unauthorized access'
            }
        )

    def test_change_name(self):
        """Test changing name."""
        self.register()
        self._edit_user(self.user_name_2)
        self.logout()
        user = self.login(name=self.user_name_2)
        self.assertEqual(user['name'], self.user_name_2, "Wrong name")

    def test_change_name_into_duplicate(self):
        """Try change name into one, that is already exists."""
        self.register()
        self.logout()
        self.register(name=self.user_name_2)
        self._edit_user(
            name=self.user_name,
            result={'status': 'user exists'}
        )

    def test_change_password(self):
        """Test changing password."""
        self.register()
        self._edit_user(
            self.user_name,
            old_pass=self.user_password,
            new_pass=self.user_password_2
        )
        self.logout()
        self.login(
            password=self.user_password,
            result={'status': 'wrong password'},
            code=401
        )
        self.login(password=self.user_password_2)

    def test_change_password_with_wrong_passwod(self):
        """Test changing password with wrong current password."""
        self.register()
        self._edit_user(
            name=self.user_name,
            old_pass=self.user_password_2,
            new_pass=self.user_password,
            result={'status': 'wrong password'},
            code=401
        )
        self.logout()
        self.login(
            password=self.user_password_2,
            result={"status": "wrong password"},
            code=401
        )
        self.login(password=self.user_password)

    # def test_signup_with_incorrect_args(self):
    #     raise NotImplementedError()

    # def test_change_name_into_itself(self):
    #     raise NotImplementedError()

    # def test_change_password_into_itself(self):
    #     raise NotImplementedError()

    # def test_login_with_incorrect_args(self):
    #     raise NotImplementedError()

    # def test_edit_with_incorrect_args(self):
    #     raise NotImplementedError()

    # def test_signup_with_too_long_name(self):
    #     raise NotImplementedError()

    # def test_signup_with_too_long_password(self):
    #     raise NotImplementedError()

    # def test_change_name_into_too_long_one(self):
    #     raise NotImplementedError()

    # def test_change_password_into_too_long_one(self):
    #     raise NotImplementedError()
