import time

from features_collector.postgres.postgres_connection import logs_pg_connection

pg_connection = logs_pg_connection()


# Получение позиции последнего прочитанного байта
def get_last_position():
    cursor = pg_connection.cursor()
    cursor.execute("SELECT last_position FROM last_upload_position_in_log WHERE file_name = 'app.log'")
    result = cursor.fetchone()
    cursor.close()
    return result[0] if result else 0


# Обновление позиции последнего прочитанного байта
def update_last_position(position):
    cursor = pg_connection.cursor()
    cursor.execute("UPDATE last_upload_position_in_log SET last_position = %s WHERE file_name = 'app.log'", (position,))
    pg_connection.commit()
    cursor.close()


# Открытие файла логов в режиме чтения
with open('app.log', 'r') as log_file:
    # Получение позиции последнего прочитанного байта
    last_position = get_last_position()
    print(last_position)
    while True:
        # Перемещение указателя чтения на последнюю позицию
        log_file.seek(last_position)

        new_logs = []
        max_logs = 0
        for line in log_file:
            print('new line:', line)
            log_parts = line.strip().split(' - ')
            if len(log_parts) == 4:
                log_time_str, level, req_id, message = log_parts
                log_time = time.strptime(log_time_str, '%Y-%m-%d %H:%M:%S,%f')
                log_time = time.strftime('%Y-%m-%d %H:%M:%S', log_time)  # Преобразование времени в правильный формат
                new_logs.append((log_time, level, req_id, message))
            else:
                print('error: wrong format')
            print('new_logs: {}'.format(max_logs))
            max_logs += 1
            if max_logs >= 100:
                max_logs = 0
                break

        # Загрузка новых записей в базу данных
        if new_logs:
            print('connection', pg_connection)
            cursor = pg_connection.cursor()
            insert_query = "INSERT INTO logs (log_time, level, req_id, message) VALUES (%s, %s, %s, %s)"
            cursor.executemany(insert_query, new_logs)

            cursor.execute("""
                    INSERT INTO last_upload_position_in_log (file_name, last_position)
                    VALUES (%s, %s)
                    ON CONFLICT (file_name)
                    DO UPDATE SET last_position = EXCLUDED.last_position;
                    """, ('app.log', last_position))
            pg_connection.commit()
            last_position = log_file.tell()

            cursor.close()

        time.sleep(5)
