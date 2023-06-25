import datetime
import threading

import requests

url = 'http://51.250.21.70:8000/predict-bank-quality?lat=123&long=34'


def f():
    while True:
        now = datetime.datetime.now()
        for i in range(1000):
            if i % 100 == 0:
                print(i)
            r = requests.get(url)
            print(f"Status Code: {r.status_code}, Content: {r.text}")
        print(datetime.datetime.now() - now)


t1 = threading.Thread(target=f)
t1.start()
