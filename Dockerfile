# Используем официальный образ Python в качестве основы
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

WORKDIR /app
# Копирование приложения в контейнер
COPY . /app

# Установка зависимостей
RUN pip freeze > requirements.txt .
RUN pip install -r ./requirements.txt