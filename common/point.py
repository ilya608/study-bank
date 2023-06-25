from sqlalchemy import Column, Float, String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


# Определяем класс для таблицы "points"
class Point(Base):
    __tablename__ = "points"

    id = Column(Float, primary_key=True)
    latitude = Column(Float)
    longitude = Column(Float)
    building_type = Column(String)
