import requests
from concurrent.futures import ThreadPoolExecutor

url = 'http://51.250.21.70:8000/predict-bank-quality'

# Параметры запроса
params = {
    'lat': '43',
    'long': '54',
    'atm_group': 'АК Барс',
    'city': '122-й квартал',
    'region': 'Central Federal District',
    'state': 'Altai Krai'
}

# Функция для отправки запросов
def send_requests(url, params):
    while True:
        try:
            response = requests.get(url, params=params)
            print(f"Response: {response.text}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

# Создание пула потоков
with ThreadPoolExecutor(max_workers=16) as executor:
    # Запуск функции отправки запросов в каждом потоке
    for _ in range(16):
        executor.submit(send_requests, url, params)
