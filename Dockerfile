# Используем официальный образ Python в качестве основы
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Копирование приложения и файла зависимостей в контейнер

COPY . /app/
WORKDIR /app
# Установка зависимостей
RUN pip install -r requirements.txt

RUN mkdir --parents ~/.postgresql && wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" --output-document ~/.postgresql/root.crt && chmod 0600 ~/.postgresql/root.crt