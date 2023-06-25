import datetime
import threading
import time

import requests

url = 'http://51.250.21.70:8000/predict-bank-quality?debug=false&lat=34&long=25&atm_group=1022&city=122-%D0%B9%20%D0%BA%D0%B2%D0%B0%D1%80%D1%82%D0%B0%D0%BB&region=Central%20Federal%20District&state=Altai%20Krai'


def f():
    while True:
        now = datetime.datetime.now()
        for i in range(100):
            r = requests.get(url)
            if i % 100 == 0:
                print(i)
                print(f"Status Code: {r.status_code}, Content: {r.text}")
        print(datetime.datetime.now() - now)
        time.sleep(0.2)


t1 = threading.Thread(target=f)
t1.start()
