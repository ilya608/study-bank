import csv

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from common.point import Point

Base = declarative_base()


class PostgresPointsTableInitializer:
    def __init__(self, csv_file_path, db_url):
        self.csv_file_path = csv_file_path
        self.db_url = db_url

    def create_table(self):
        engine = create_engine(self.db_url)
        Base.metadata.create_all(engine)

    def fill_table(self):
        # Открываем CSV файл и читаем данные
        with open(self.csv_file_path, "r") as csvfile:
            reader = csv.reader(csvfile)
            next(reader)  # пропускаем заголовок
            data = [(float(row[0]), float(row[1]), row[2]) for row in reader]

        # Создаем сессию для работы с базой данных
        engine = create_engine(self.db_url)
        Session = sessionmaker(bind=engine)
        session = Session()

        session.query(Point).delete()

        # Заполняем таблицу данными из CSV файла
        for id, (latitude, longitude, building_type) in enumerate(data):
            point = Point(id=id, latitude=latitude, longitude=longitude, building_type=building_type)
            session.add(point)

        session.commit()


if __name__ == "__main__":
    initializer = PostgresPointsTableInitializer(csv_file_path="points.csv",
                                                 db_url="postgresql://postgres:abc@localhost:5432/points")
    initializer.create_table()
    initializer.fill_table()
