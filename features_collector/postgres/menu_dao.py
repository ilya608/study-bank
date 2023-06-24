class MenuDao:
    def __init__(self, connection):
        self.connection = connection

    def get_menu_data(self):
        cursor = self.connection.cursor()

        query = 'SELECT avg_feature, avg_type, target from avg_table'

        cursor.execute(query)
        pg_result = cursor.fetchall()

        self.connection.commit()
        cursor.close()

        result = {}
        for row in pg_result:
            if row[1] not in result:
                result[row[1]] = [row[0]]
            else:
                result[row[1]].append(row[0])

        for item in result:
            result[item] = sorted(result[item])

        return result
