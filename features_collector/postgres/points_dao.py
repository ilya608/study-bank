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

    # методы пока не работают
    # def get_cnt_apart(self, lat, lon):
    #     return self.get_cnt(self, lat, lon, 'apart')
    #
    # def get_cnt_atm(self, lat, lon):
    #     return self.get_cnt(self, lat, lon, 'atm')
    #
    # def get_cnt_bank(self, lat, lon):
    #     return self.get_cnt(self, lat, lon, 'bank')
    #
    # def get_cnt(self, lat, lon, like_obj):
    #     cursor = self.connection.cursor()
    #
    #     query = f"""SELECT COUNT() AS cnt_atm_200m FROM points
    #                 WHERE
    #                 (latitude111111.11 => {lat}111111.11 - 200)
    #                 AND (latitude111111.11 =< {lat}111111.11 + 200)
    #                 AND (longitude111111.11COS(latitude) => {lon}111111.11COS({lat}) - 200)
    #                 AND (longitude111111.11COS(latitude) =< {lon}COS({lat})*111111.11 + 200)
    #                 AND building_type LIKE '%{like_obj}%' """
    #
    #     cursor.execute(query)
    #     result = cursor.fetchall()
    #
    #     self.connection.commit()
    #     cursor.close()
    #
    #     return result[0][0]
