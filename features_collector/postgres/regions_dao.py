class RegionsDao:
    def __init__(self, connection):
        self.connection = connection


def get_regions_data(self, region, logger, req_id):
    cursor = self.connection.cursor()

    query = '''SELECT regions, population, salary, population_density, happy_index
            FROM regions_table WHERE regions = {}'''.format(region)


    try:
        cursor.execute(query)
        result = cursor.fetchall()

        self.connection.commit()
        cursor.close()

        dd = {}

        for row in result:
            dd['population'] = row[1]
            dd['salary'] = row[2]
            dd['population_density'] = row[3]
            dd['happy_index'] = row[4]
            break

        return dd
    except Exception as e:
            logger.error('failed regions dao query {}'.format(e),
                         extra={'reqId': req_id})

            # todo
            print(3)
    finally:
            cursor.close()