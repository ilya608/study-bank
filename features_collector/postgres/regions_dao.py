class RegionsDao:
    def __init__(self, connection):
        self.connection = connection

    def get_regions_data(self, region, logger, req_id):
        cursor = self.connection.cursor()

        query = """
                SELECT region, population, salary, population_density, happy_index 
                FROM regions_table
                WHERE region = '{}'
                """.format(region)

        try:
            cursor.execute(query)
            result = cursor.fetchall()

            self.connection.commit()

            dd = {}

            dd['population'] = result[0][1]
            dd['salary'] = result[0][2]
            dd['population_density'] = result[0][3]
            dd['happy_index'] = result[0][4]

            return dd
        except Exception as e:
            logger.error('failed regions dao query {}'.format(e),
                         extra={'reqId': req_id})
            self.connection.rollback()
        finally:
            cursor.close()
