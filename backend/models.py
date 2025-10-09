from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from database import Base
from datetime import datetime, date
from sqlalchemy.orm import relationship


class City(Base):
    __tablename__ = "cities"
    id=Column(Integer, primary_key=True,index=True)
    name=Column(String, index=True)
    country=Column(String)
    lat=Column(Float)
    lon=Column(Float)
    created_at=Column(DateTime,default=datetime.utcnow)

    weather_desc = relationship("WeatherDesc", back_populates="city")

class WeatherDesc(Base):
    __tablename__ = "weather_desc"
    id=Column(Integer, primary_key=True,index=True)
    city_id=Column(Integer,ForeignKey("cities.id"))
    temperature=Column(Float)
    humidity=Column(Float)
    wind_speed=Column(Integer)
    description=Column(String)
    date=Column(DateTime, default=datetime.utcnow, index=True)
    min_temp = Column(Float),
    max_temp = Column(Float),
    overview = Column(String)

    city = relationship("City", back_populates="weather_desc")