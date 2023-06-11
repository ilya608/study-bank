# Используем официальный образ Python в качестве основы
#FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
FROM python:3.9

# Копирование приложения и файла зависимостей в контейнер

WORKDIR /app
COPY logs .
COPY features_collector ./features_collector

# Установка зависимостей
RUN pip install -r requirements.txt

CMD ["python3", "dump_to_postgres.py"]