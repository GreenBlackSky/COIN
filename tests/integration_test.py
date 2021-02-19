"""Some test methods."""

import unittest
import requests


class Integration(unittest.TestCase):
    """Class for coin tests."""

    HOST = "http://localhost:5002/"

    def test_access(self):
        """Check if every service is up and accessible."""
        response = requests.post(url=self.HOST+"access_test")
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertDictEqual(
            response.json(),
            {'access': 'ok'},
            "Wrong answear"
        )

    def test_connection(self):
        """Check if every service is up and accessible."""
        response = requests.post(url=self.HOST+"connection_test")
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertDictEqual(
            response.json(),
            {'redis_val': 'ok', 'postgres_val': 'ok'},
            "Wrong answear"
        )

    def test_redis(self):
        """Try setting value in redis."""
        response = requests.post(
            url=self.HOST+"test_set_redis_value",
            json={'key': 99, 'val': "!"}
        )
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertDictEqual(
            response.json(),
            {'99': '!'},
            "Wrong answear"
        )
        response = requests.post(
            url=self.HOST+"test_get_redis_value",
            json={'key': 99}
        )
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertDictEqual(
            response.json(),
            {'99': '!'},
            "Wrong answear"
        )

    def test_postgres(self):
        """Try setting value in postgres and getting it back."""
        response = requests.post(
            url=self.HOST+"test_set_postgres_value",
            json={'val': "?"}
        )
        self.assertEqual(response.status_code, 200, "Wrong response code")
        key, val = list(response.json().items())[0]
        self.assertEqual(val, '?', "Wrong value")

        response = requests.post(
            url=self.HOST+"test_get_postgres_value",
            json={'key': key}
        )
        self.assertEqual(response.status_code, 200, "Wrong response code")
        self.assertDictEqual(
            response.json(),
            {key: '?'},
            "Wrong answear"
        )
