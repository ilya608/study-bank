import csv

from psycopg2.extras import execute_batch


class PostgresRegionsTableInitializer:
    def __init__(self, connection):
        self.connection = connection

    def clear_table(self):
        cursor = self.connection.cursor()

        cursor.execute("drop table regions_table")
        self.connection.commit()
        cursor.close()

    def create_regions_table(self):
        cursor = self.connection.cursor()

        cursor.execute(
            "SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'regions_table')")
        table_exists = cursor.fetchone()[0]

        if table_exists:
            print("Таблица regions_table уже существует")
            self.clear_table()
        # Создание таблицы avg_table
        create_table_query = """
                    CREATE TABLE regions_table (
                        region varchar,
                        population float,
                        salary float,
                        population_density float,
                        happy_index float 
                    )
                    """
        cursor.execute(create_table_query)

        self.connection.commit()
        print("Таблица regions_table создана")

        self.fill_table()

        cursor.close()
        return 0

    def fill_table(self):
        with open('avg_table/regions_data.csv', 'r') as file:
            # Создание объекта DictReader для чтения CSV-файла
            reader = csv.DictReader(file)

            # Создание курсора
            cursor = self.connection.cursor()
            batch = []
            batch_counter = 0
            BATCH_SIZE = 100000
            # Вставка данных из CSV-файла в таблицу regions_table
            for row in reader:
                region = row['region']

                if region[0] == "'":
                    region = region[1:]
                if region[-1] == "'":
                    region = region[:-1]
                batch.append(
                    (region, row['population'], row['salary'], 
                    row['population_density'], row['happy_index']))

                if len(batch) == BATCH_SIZE:
                    execute_batch(cursor, """
                                INSERT INTO regions_table (region, population, salary, population_density, happy_index)
                                VALUES (%s, %s, %s, %s, %s)
                            """, batch)
                    self.connection.commit()
                    batch_counter += 1
                    batch = []
                    print('Batch write ok {}'.format(batch_counter))
            if len(batch) > 0:
                execute_batch(cursor, """
                                    INSERT INTO regions_table (region, population, salary, population_density, happy_index)
                                    VALUES (%s, %s, %s, %s, %s)
                                """, batch)
            # Фиксация изменений
            self.connection.commit()

            # Закрытие курсора
            cursor.close()

        print("Данные из файла regions_data.csv успешно загружены в таблицу regions_table")
