class PointsDao:
    def __init__(self, connection):
        self.connection = connection

    def get_nearest_points(self, lat, lon, logger, req_id):
        cursor = self.connection.cursor()
        try:
            query = 'SELECT building_type, MIN(distance) AS min_distance ' \
                    'FROM (SELECT building_type, latitude, longitude, ' \
                    'sqrt(pow((latitude - {lat}), 2) + pow((longitude - {lon}), 2)) AS distance ' \
                    'FROM points limit 1000) AS subquery ' \
                    'GROUP BY building_type'.format(lat=lat, lon=lon)

            cursor.execute(query)
            result = cursor.fetchall()
            self.connection.commit()
            return [{'building_type': row[0],
                     'min_distance': row[1]} for row in result]
        except Exception as e:
            logger.error('failed points dao query {}'.format(e), extra={'reqId': req_id})

        finally:
            cursor.close()

    def get_cnt200m_points(self, latitude, longitude, logger, req_id):
        cursor = self.connection.cursor()

        query = """
                SELECT building_type, COUNT(*)
                FROM points
                WHERE
                    (ACOS(SIN(RADIANS(latitude)) * SIN(RADIANS({})) + COS(RADIANS(latitude)) * COS(RADIANS({})) * COS(RADIANS({} - longitude)))) * 6371000 <= 200
                GROUP BY building_type;
            """.format(latitude, latitude, longitude)
        try:
            cursor.execute(query)

            result = {}
            for row in cursor:
                building_type = row[0]
                count = row[1]
                result[building_type] = count
            return result
        except Exception as e:
            logger.error('failed cnt200m dao query {}'.format(e), extra={'reqId': req_id})

            self.connection.rollback()
        finally:
            cursor.close()