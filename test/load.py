import datetime
import random
from time import sleep

import requests
import grequests

url = 'http://51.250.21.70:8000/predict-bank-quality?lat=123&long=34'


while True:
    now = datetime.datetime.now()
    for i in range(100):
        r = [grequests.get(url)]
        # print(f"Status Code: {r.status_code}, Content: {r.json()}")
    print(datetime.datetime.now() - now)
    sleep(0.1)