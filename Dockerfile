# Используем официальный образ Python в качестве основы
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Копирование приложения и файла зависимостей в контейнер

COPY . /app/

# Установка зависимостей
RUN pip install -r /app/requirements.txt
