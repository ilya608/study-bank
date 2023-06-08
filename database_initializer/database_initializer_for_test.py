import csv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from common.point import Point
from features_collector.postgres.postgres_connection import get_pg_connection


class PostgresPointsTableInitializer:
    def __init__(self, connection):
        self.connection = connection

    def clear_table(self):
        cursor = self.connection.cursor()

        cursor.execute("drop table points")
        self.connection.commit()
        cursor.close()

    def create_table(self):
        cursor = self.connection.cursor()

        cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'points')")
        table_exists = cursor.fetchone()[0]

        if not table_exists:
            # Создание таблицы points
            create_table_query = """
                CREATE TABLE points (
                    latitude float8,
                    longitude float8,
                    building_type varchar   
                )
                """
            cursor.execute(create_table_query)

            self.connection.commit()
            print("Таблица points создана")
        else:
            print("Таблица points уже существует")
            self.clear_table()
        self.fill_table()

        cursor.close()
        return 0

    def fill_table(self):
        with open('points.csv', 'r') as file:
            # Создание объекта DictReader для чтения CSV-файла
            reader = csv.DictReader(file)

            # Создание курсора
            cursor = self.connection.cursor()

            # Вставка данных из CSV-файла в таблицу points
            for row in reader:
                latitude = row['latitude']
                longitude = row['longitude']
                building_type = row['building_type']

                # Выполнение SQL-запроса для вставки данных
                cursor.execute("INSERT INTO points (latitude, longitude, building_type) VALUES (%s, %s, %s)",
                               (latitude, longitude, building_type))

            # Фиксация изменений
            self.connection.commit()

            # Закрытие курсора
            cursor.close()

        print("Данные из файла points.csv успешно загружены в таблицу points")


if __name__ == "__main__":
    pg_connection = get_pg_connection()
    initializer = PostgresPointsTableInitializer(pg_connection)

    initializer.create_table()
