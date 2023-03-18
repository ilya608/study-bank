from sqlalchemy import Engine, text
from sqlalchemy.orm import Session, sessionmaker
from typing import List

from common.point import Point


class PointsDao:
    def __init__(self, engine: Engine):
        self.engine = engine

    def get_all_points(self) -> List[Point]:
        # Создаем класс сессии
        Session = sessionmaker(bind=self.engine)
        # Создаем объект сессии
        session = Session()

        return session.query(Point).all()

    def get_nearest_points(self, lat, lon):
        # Создаем класс сессии
        Session = sessionmaker(bind=self.engine)
        # Создаем объект сессии
        session = Session()

        query = text('SELECT building_type, MIN(distance) AS min_distance '
                     'FROM (SELECT building_type, latitude, longitude, '
                     'sqrt(pow((latitude - :lat), 2) + pow((longitude - :lon), 2)) AS distance '
                     'FROM points) AS subquery '
                     'GROUP BY building_type')
        result = session.execute(query, {'lat': lat, 'lon': lon})
        return [{'building_type': row.building_type,
                 'min_distance': row.min_distance} for row in result]
