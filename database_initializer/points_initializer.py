import csv

from psycopg2.extras import execute_batch


class PostgresPointsTableInitializer:
    def __init__(self, connection):
        self.connection = connection

    def clear_table(self):
        cursor = self.connection.cursor()

        cursor.execute("drop table points")
        self.connection.commit()
        cursor.close()

    def create_table_points(self):
        cursor = self.connection.cursor()

        cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'points')")
        table_exists = cursor.fetchone()[0]

        if table_exists:
            print("Таблица points уже существует")
            self.clear_table()
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

        self.fill_table()

        cursor.close()
        return 0

    def fill_table(self):
        with open('points1.csv', 'r') as file:
            # Создание объекта DictReader для чтения CSV-файла
            reader = csv.DictReader(file)

            # Создание курсора
            cursor = self.connection.cursor()
            batch = []
            batch_counter = 0
            BATCH_SIZE = 100000
            # Вставка данных из CSV-файла в таблицу points
            for row in reader:
                batch.append((row['latitude'], row['longitude'], row['bulding_type']))

                if len(batch) == BATCH_SIZE:
                    execute_batch(cursor, """
                                INSERT INTO points (latitude, longitude, building_type)
                                VALUES (%s, %s, %s)
                            """, batch)
                    self.connection.commit()
                    batch_counter += 1
                    batch = []
                    print('Batch write ok {}'.format(batch_counter))

            # Фиксация изменений
            self.connection.commit()

            # Закрытие курсора
            cursor.close()

        print("Данные из файла points1.csv успешно загружены в таблицу points")
