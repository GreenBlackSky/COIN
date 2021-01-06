import requests


HOST = "http://localhost:5003/"


def test_connection():
    tests = [
        "access_test",
        "connection_test",
    ]

    for URL in tests:
        responce = requests.post(url=HOST+URL)
        print(URL, responce.text)


def test_redis():
    tests = {
        "test_set_redis_value": {'key': 99, 'val': "!"},
        "test_get_redis_value": {'key': 99},
    }

    for URL, params in tests.items():
        responce = requests.post(url=HOST+URL, params=params)
        print(URL, responce.text)


def test_postgres():
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


if __name__ == "__main__":
    test_connection()
    test_redis()
    test_postgres()
