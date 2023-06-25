# Используем официальный образ Python в качестве основы
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Копирование приложения и файла зависимостей в контейнер

COPY logs /app/logs
COPY features_collector /app/features_collector

WORKDIR /app

RUN pip install -r logs/requirements1.txt

RUN mkdir --parents ~/.postgresql && wget "https://storage.yandexcloud.net/cloud-certs/CA.pem" --output-document ~/.postgresql/root.crt && chmod 0600 ~/.postgresql/root.crt

#CMD ["python3", "logs/dump_to_postgres.py"]