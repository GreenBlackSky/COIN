"""Some test methods."""

import requests


HOST = "http://localhost:5003/"


def test_connection():
    """Check if every service is up and accessible."""
    tests = [
        "access_test",
        "connection_test",
    ]

    for URL in tests:
        responce = requests.post(url=HOST+URL)
        print(URL, responce.text)


def test_redis():
    """Check if redis is up and running."""
    tests = {
        "test_set_redis_value": {'key': 99, 'val': "!"},
        "test_get_redis_value": {'key': 99},
    }

    for URL, params in tests.items():
        responce = requests.post(url=HOST+URL, params=params)
        print(URL, responce.text)


def test_postgres():
    """Check if postgres up and running."""
    responce = requests.post(
        url=HOST+"test_set_postgres_value",
        params={'val': "?"}
    )
    print(responce.text)

    key = list(eval(responce.text).keys())[0]
    responce = requests.post(
        url=HOST+"test_get_postgres_value",
        params={'key': key}
    )
    print(responce.text)


def test_login():
    """Test login stuff."""
    responce = requests.post(url=HOST+"test_login")
    print(responce.text)

    responce = requests.post(
        url=HOST+"register",
        params={'name': "user", 'password': "qwerty"}
    )
    print(responce.text)

    responce = requests.post(url=HOST+"test_login")
    print(responce.text)

    responce = requests.post(url=HOST+"logout")
    print(responce.text)

    responce = requests.post(url=HOST+"test_login")
    print(responce.text)

    responce = requests.post(
        url=HOST+"login",
        params={'name': "user", 'password': "qwerty"}
    )
    print(responce.text)

    responce = requests.post(url=HOST+"test_login")
    print(responce.text)

    responce = requests.post(url=HOST+"logout")
    print(responce.text)

    responce = requests.post(
        url=HOST+"login",
        params={'name': "user", 'password': "ytrewq"}
    )
    print(responce.text)

    responce = requests.post(url=HOST+"test_login")
    print(responce.text)

    responce = requests.post(
        url=HOST+"register",
        params={'name': "user", 'password': "ytrewq"}
    )
    print(responce.text)

    responce = requests.post(url=HOST+"test_login")
    print(responce.text)


if __name__ == "__main__":
    test_connection()
    test_redis()
    test_postgres()
    test_login()
