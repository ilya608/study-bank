# Используем официальный образ Python в качестве основы
FROM tiangolo/uvicorn-gunicorn-fastapi:python3.8

# Копирование приложения в контейнер
COPY ./app.py /app

# Установка зависимостей
RUN pip freeze > requirements.txt .
RUN pip install -r ./requirements.txt