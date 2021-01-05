import requests

HOST = "http://localhost:5003/"

tests = {
    "access_test": {},
    "connection_test": {},
    "test_set_redis_value": {'key': 99, 'val': "!"},
    "test_get_redis_value": {'key': 99},
    "test_set_postgres_value": {'val': "?"},
    "test_get_postgres_value": {'key': 0},
}


for URL, params in tests.items():
    responce = requests.post(url=HOST+URL, params=params)
    print(URL, responce.text)
