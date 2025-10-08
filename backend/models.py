from sqlalchemy import Column, Integer, String, Float, DateTime, ForeignKey
from database import Base
from DateTime import datetime
from sqlalchemy.orm import relationship


class City(Base):
    __tablename__ = "cities"
    id=Column(Integer, primary_key=True,index=True)
    name=Column(String, index=True)
    country=Column(String)
    lat=Column(Float)
    lon=Column(Float)
    created_at=Column(DateTime, default=datetime.utnowm)

    weather_desc = relationship("weatherDesc", back_populate="city")

class WeatherDesc(Base):
    __tablename__ = "weather_desc"
    id=Column(Integer, primary_key=True,index=True)
    city_id=Column(Integer,ForeignKey("cities.id"))
    temperature=Column(Float)
    humidity=Column(Float)
    wind_speed=Column(Integer)
    description=Column(String)
    date=Column(DateTime, index=True)

    city = relationship("city", back_populate="weatherDesc")