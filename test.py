"""Some test methods."""

import unittest
import requests


class Integration(unittest.TestCase):
    """Class for coin tests."""

    HOST = "http://localhost:5003/"

    def setUp(self):
        """Set test values."""
        self._user_name = "user1"
        self._user_password = "pass1"
        self._wrong_user_password = "ass1"
        self._duplicate_user_name = "user2"
        self._duplicate_user_password = "pass2"

    def test_access(self):
        """Check if every service is up and accessible."""
        responce = requests.post(url=self.HOST+"access_test")
        self.assertEqual(responce.status_code, 200, "Wrong responce code")
        self.assertDictEqual(responce.json(), {'access': 'ok'}, "Wrong answear")

    def test_connection(self):
        """Check if every service is up and accessible."""
        responce = requests.post(url=self.HOST+"connection_test")
        self.assertEqual(responce.status_code, 200, "Wrong responce code")
        self.assertDictEqual(
            responce.json(),
            {'redis_val': 'ok', 'postgres_val': 'ok'},
            "Wrong answear"
        )

    def test_set_redis_value(self):
        """Try setting value in redis."""
        responce = requests.post(
            url=self.HOST+"test_set_redis_value",
            params={'key': 99, 'val': "!"}
        )
        self.assertEqual(responce.status_code, 200, "Wrong responce code")
        self.assertDictEqual(
            responce.json(),
            {'99': '!'},
            "Wrong answear"
        )

    def test_get_redis_value(self):
        """Try getting value from redis."""
        responce = requests.post(
            url=self.HOST+"test_get_redis_value",
            params={'key': 99}
        )
        self.assertEqual(responce.status_code, 200, "Wrong responce code")
        self.assertDictEqual(
            responce.json(),
            {'99': '!'},
            "Wrong answear"
        )

    def test_postgres(self):
        """Try setting value in postgres and getting it back."""
        responce = requests.post(
            url=self.HOST+"test_set_postgres_value",
            params={'val': "?"}
        )
        self.assertEqual(responce.status_code, 200, "Wrong responce code")
        key, val = list(responce.json().items())[0]
        self.assertEqual(val, '?', "Wrong value")

        responce = requests.post(
            url=self.HOST+"test_get_postgres_value",
            params={'key': key}
        )
        self.assertEqual(responce.status_code, 200, "Wrong responce code")
        self.assertDictEqual(
            responce.json(),
            {key: '?'},
            "Wrong answear"
        )

    def test_unautharized(self):
        """Try unautharized access to app."""
        responce = requests.post(url=self.HOST+"test_login")
        self.assertEqual(responce.status_code, 200, "Wrong responce code")
        self.assertDictEqual(
            responce.json(),
            {"status": "Unauthorized access"},
            "Wrong answear"
        )

    def test_register(self):
        responce = requests.post(
            url=self.HOST+"register",
            params={'name': self._user_name, 'password': self._user_password}
        )
        self.assertEqual(responce.status_code, 200, "Wrong responce code")
        self.assertDictEqual(responce.json(), {'status': 'OK'}, "Wrong answear")

        responce = requests.post(url=self.HOST+"test_login")
        self.assertEqual(responce.status_code, 200, "Wrong responce code")
        self.assertDictContainsSubset(
            {'status': "OK"},
            responce.json(),
            "Wrong answear"
        )

        responce = requests.post(url=self.HOST+"logout")
        self.assertEqual(responce.status_code, 200, "Wrong responce code")
        self.assertDictEqual(responce.json(), {'status': 'OK'}, "Wrong answear")

    def test_login(self):
        responce = requests.post(
            url=self.HOST+"login",
            params={'name': self._user_name, 'password': self._user_password}
        )
        print(responce.text)

        responce = requests.post(url=self.HOST+"test_login")
        print(responce.text)

        responce = requests.post(url=self.HOST+"logout")
        print(responce.text)

    def test_wrong_password(self):
        responce = requests.post(
            url=self.HOST+"login",
            params={'name': "user", 'password': "ytrewq"}
        )
        print(responce.text)

        responce = requests.post(url=self.HOST+"test_login")
        print(responce.text)

    def test_duplicate_register(self):
        responce = requests.post(
            url=self.HOST+"register",
            params={'name': "user", 'password': "ytrewq"}
        )
        print(responce.text)

        responce = requests.post(
            url=self.HOST+"register",
            params={'name': "user", 'password': "ytrewq"}
        )
