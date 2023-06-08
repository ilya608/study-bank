from sqlalchemy import Engine, text
from sqlalchemy.orm import Session, sessionmaker
from typing import List

from common.point import Point
from features_collector.postgres.postgres_connection import get_pg_connection


class PointsDao:
    def __init__(self, connection):
        self.connection = connection

    def get_nearest_points(self, lat, lon):
        cursor = self.connection.cursor()

        query = 'SELECT building_type, MIN(distance) AS min_distance ' \
                'FROM (SELECT building_type, latitude, longitude, ' \
                'sqrt(pow((latitude - {lat}), 2) + pow((longitude - {lon}), 2)) AS distance ' \
                'FROM points) AS subquery ' \
                'GROUP BY building_type'.format(lat=lat, lon=lon)

        cursor.execute(query)
        result = cursor.fetchall()

        self.connection.commit()
        cursor.close()

        return [{'building_type': row[0],
                 'min_distance': row[1]} for row in result]
