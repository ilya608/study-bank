import uuid


class LogsDao:
    def __init__(self, connection):
        self.connection = connection

    def select_logs(self, req_id):
        try:
            uuid.UUID(req_id)
            cursor = self.connection.cursor()
            query = "select * from logs where req_id='{}'".format(req_id)
            cursor.execute(query)
            result = cursor.fetchall()
            self.connection.commit()
            cursor.close()
        except Exception:
            return []

        return result
