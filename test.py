import requests


tests = {
    "http://localhost:5003/easy_test": {},
    "http://localhost:5003/simple_test": {},
    "http://localhost:5003/test_set_redis_value": {'key': 99, 'val': "!"},
    "http://localhost:5003/test_get_redis_value": {'key': 99},
}


for URL, params in tests.items():
    responce = requests.post(url=URL, params=params)
    print(responce.text)
