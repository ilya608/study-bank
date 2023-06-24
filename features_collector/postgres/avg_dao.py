class AvgDao:
    def __init__(self, connection):
        self.connection = connection

    def get_avg_features_data(self, atm_group, city, region, state, logger, req_id):
        cursor = self.connection.cursor()
        atm_group = str(atm_group)

        query = """
        SELECT *
        FROM avg_table
        WHERE (avg_type = 'atm_group' AND avg_feature = '{}')
           OR (avg_type = 'cities' AND avg_feature = '{}')
           OR (avg_type = 'regions' AND avg_feature = '{}')
           OR (avg_type = 'states' AND avg_feature = '{}');
        """.format(int(float(atm_group)), city, region, state)

        try:
            cursor.execute(query)
            result = cursor.fetchall()
            self.connection.commit()

            dd = {}
            for row in result:
                if row[0] == str(int(float(atm_group))):
                    dd['atm_group'] = row[2]
                elif row[0] == city:
                    dd['cities'] = row[2]
                elif row[0] == region:
                    dd['regions'] = row[2]
                elif row[0] == state:
                    dd['states'] = row[2]

            return dd
        except Exception as e:
            logger.error('failed avg dao query {}'.format(e), extra={'reqId': req_id})

            # todo
            print(3)
        finally:
            cursor.close()
