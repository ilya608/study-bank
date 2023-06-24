import csv

from psycopg2.extras import execute_batch


class PostgresAvgTableInitializer:
    def __init__(self, connection):
        self.connection = connection

    def clear_table(self):
        cursor = self.connection.cursor()

        cursor.execute("drop table avg_table")
        self.connection.commit()
        cursor.close()

    def create_avg_table(self):
        cursor = self.connection.cursor()

        cursor.execute("SELECT EXISTS (SELECT 1 FROM information_schema.tables WHERE table_name = 'avg_table')")
        table_exists = cursor.fetchone()[0]

        if table_exists:
            print("Таблица avg_table уже существует")
            self.clear_table()
        # Создание таблицы avg_table
        create_table_query = """
                    CREATE TABLE avg_table (
                        avg_feature varchar,
                        avg_type varchar,
                        target varchar   
                    )
                    """
        cursor.execute(create_table_query)

        self.connection.commit()
        print("Таблица avg_table создана")

        self.fill_table()

        cursor.close()
        return 0

    def fill_table(self):
        with open('avg_table/avg_table.csv', 'r') as file:
            # Создание объекта DictReader для чтения CSV-файла
            reader = csv.DictReader(file)

            # Создание курсора
            cursor = self.connection.cursor()
            batch = []
            batch_counter = 0
            BATCH_SIZE = 100000
            # Вставка данных из CSV-файла в таблицу avg_table
            for row in reader:
                avg_feature = row['avg_feature']
                avg_type = row['avg_type']

                if avg_feature[0] == "'":
                    avg_feature = avg_feature[1:]
                if avg_feature[-1] == "'":
                    avg_feature = avg_feature[:-1]
                if avg_type[0] == "'":
                    avg_type = avg_type[1:]
                if avg_type[-1] == "'":
                    avg_type = avg_type[:-1]
                batch.append((avg_feature, avg_type, row['target']))

                if len(batch) == BATCH_SIZE:
                    execute_batch(cursor, """
                                INSERT INTO avg_table (avg_feature, avg_type, target)
                                VALUES (%s, %s, %s)
                            """, batch)
                    self.connection.commit()
                    batch_counter += 1
                    batch = []
                    print('Batch write ok {}'.format(batch_counter))
            if len(batch) > 0:
                execute_batch(cursor, """
                                    INSERT INTO avg_table (avg_feature, avg_type, target)
                                    VALUES (%s, %s, %s)
                                """, batch)
            # Фиксация изменений
            self.connection.commit()

            # Закрытие курсора
            cursor.close()

        print("Данные из файла avg_table.csv успешно загружены в таблицу avg_table")
