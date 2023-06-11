# Используем официальный образ Python в качестве основы
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8
FROM python:3.9

# Копирование приложения и файла зависимостей в контейнер

COPY . /app/

# Установка зависимостей
RUN pip install -r /app/requirements.txt

#CMD ['python3', 'logs/dump_to_postgres.py']