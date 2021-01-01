import requests


URLs = [
    "http://localhost:5003/easy_test",
    "http://localhost:5003/simple_test"
]

for URL in URLs:
    responce = requests.post(url=URL)
    print(responce.text)
