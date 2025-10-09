from fastapi import FastAPI, Depends, Query
from fastapi.responses import JSONResponse
import os, requests
from dotenv import load_dotenv
from datetime import datetime
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import City,WeatherDesc, Base

class cityCreate(BaseModel):
    city:str
    country: str
    created_at: datetime | None = None
# Base.metadata.drop_all(bind=engine)
#create table if not exist
Base.metadata.create_all(bind=engine)

#load env
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = FastAPI()
origins = [
    "http://localhost:3000",   # React dev server
    "http://127.0.0.1:3000",   # sometimes React uses this
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],            # list of allowed origins
    allow_credentials=True,
    allow_methods=["*"],              # allow all HTTP methods (GET, POST, etc.)
    allow_headers=["*"],              # allow all headers
)

#get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/city")
def add_city(data: cityCreate,db: Session = Depends(get_db)):
    """Fetch current weather for a given city and country"""

    #Get latitude and longitude
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={data.city},{data.country}&appid={API_KEY}"
    geo_resp = requests.get(geo_url)
    geo_data = geo_resp.json()

    if not geo_data:
        return {"error": "City not found. Check spelling or try another city."}

    lat, lon = geo_data[0]["lat"], geo_data[0]["lon"]
    created_at = data.created_at or datetime.utcnow()

    # #check if city alredy exsists
    # db_city = db.query(City).filter(City.name == data.city, City.country == data.country, City.created_at == created_at).first()
    # if db_city:
    #     return {"message": "City was created alredy at this time", "city": db_city.name, "lat": db_city.lat, "lon": db_city.lon}

    #Save to db
    new_city = City(name=data.city, country=data.country, lat=lat, lon=lon, created_at=created_at)
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return {"message": "City added successfully", "city": data.city, "lat": lat, "lon": lon, "created_at": created_at.isoformat()}
    
@app.get("/weather")
def get_weather(city: str, country: str, db: Session = Depends(get_db)):

    db_city = db.query(City).filter(City.name == city, City.country == country).first()
    if not db_city:
        return {"error":"city not found, please add it first."}
    
    #Get current weather
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={db_city.lat}&lon={db_city.lon}&appid={API_KEY}&units=metric"
    weather_res = requests.get(weather_url)
    weather_data = weather_res.json()

    if weather_res.status_code != 200:
        return {"Error": "Failed to fetch weather data."}
    
    #save to DB
    new_weather = WeatherDesc(
        city_id=db_city.id,
        temperature=weather_data["main"]["temp"],
        humidity=weather_data["main"]["humidity"],
        wind_speed=weather_data["wind"]["speed"],
        description=weather_data["weather"][0]["description"],
        date=datetime.utcnow()
        )
    
    db.add(new_weather)
    db.commit()
    db.refresh(new_weather)
    
    #return data
    return JSONResponse(content={
        "city":db_city.name,
        "country": db_city.country,
        "temperature": weather_data["main"]["temp"],
        "feels_like": weather_data["main"]["feels_like"],
        "humidity": weather_data["main"]["humidity"],
        "description": weather_data["weather"][0]["description"],
        "wind_speed": weather_data["wind"]["speed"],
        "date": new_weather.date.isoformat()
    })

#get weather by timestamp
@app.get("/weather/timestamp")
def get_weather_by_time(city: str,country:str, date_time:datetime, db: Session = Depends(get_db)):

    db_city = db.query(City).filter(City.name == city, City.country == country).first()
    if not db_city:
        return {"error":"city not found, please add it first."}
    
    weather_time_url = f"https://api.openweathermap.org/data/3.0/onecall/timemachine?lat={db_city.lat}&lon={db_city.lon}&dt={db_city.created_at}&appid={API_KEY}&units=metric"
    weather_time_res = requests.get(weather_time_url)
    weather_time_data = weather_time_res.json()

    if weather_time_res.status_code != 200:
        return {"Error": "Failed to fetch weather data."}
    
    #save to DB
    new_weather = WeatherDesc(
        city_id=db_city.id,
        temperature=weather_time_data["main"]["temp"],
        humidity=weather_time_data["main"]["humidity"],
        wind_speed=weather_time_data["wind"]["speed"],
        description=weather_time_data["weather"][0]["description"],
        date=weather_time_data["dt"]
        )
    
    db.add(new_weather)
    db.commit()
    db.refresh(new_weather)

    #return data
    return{
        "city":db_city.name,
        "country": db_city.country,
        "temperature": weather_time_data["main"]["temp"],
        "feels_like": weather_time_data["main"]["feels_like"],
        "humidity": weather_time_data["main"]["humidity"],
        "description": weather_time_data["weather"][0]["description"],
        "wind_speed": weather_time_data["wind"]["speed"]
    }

@app.get("/weather/date")
def get_weather_by_date(city:str,country:str,date:str ,db:Session = Depends(get_db)):
    db_city = db.query(City).filter(City.name == city, City.country == country).first()
    if not db_city:
        return {"error":"city not found, please add it first."}
    # date = db_city.created_at.date()
    
    url = "https://api.openweathermap.org/data/3.0/onecall/day_summary"
    params = {
        "lat": db_city.lat,
        "lon": db_city.lon,
        "date": date,      # Format: YYYY-MM-DD
        "appid": API_KEY,
        "units":"metric"
    }
    weather_date_res = requests.get(url, params=params)
    weather_date_data = weather_date_res.json()

    if weather_date_res.status_code != 200:
        return {"Error": "Failed to fetch weather data."}
    
    #save to DB
    new_weather = WeatherDesc(
        city_id=db_city.id,
        temperature=weather_date_data["temperature"]["afternoon"],
        humidity=weather_date_data["humidity"]["afternoon"],
        wind_speed=weather_date_data["wind"]["max"]["speed"],
        # description=weather_date_data["main"]["cloud_cover"],
        date=weather_date_data["date"],
        min_temp = weather_date_data["temperature"]["min"],
        max_temp = weather_date_data["temperature"]["max"]
        )
    
    db.add(new_weather)
    db.commit()
    db.refresh(new_weather)

     #return data
    return{
        "city":db_city.name,
        "country": db_city.country,
        "Date": weather_date_data["date"],
        "temperature": weather_date_data["temperature"]["afternoon"],
        "humidity": weather_date_data["humidity"]["afternoon"],
        # "description": weather_date_data["weather"][0]["description"],
        "wind_speed": weather_date_data["wind"]["max"]["speed"],
        "min_temp": weather_date_data["temperature"]["min"],
        "max_temp": weather_date_data["temperature"]["max"]
    }

@app.get("/weather/overview")
def get_weather_overview(city:str,country:str, db:Session = Depends(get_db)):

    db_city = db.query(City).filter(City.name == city, City.country == country).first()
    if not db_city:
        return {"error":"city not found, please add it first."}
   
    
    weather_date_url = f"https://api.openweathermap.org/data/3.0/onecall/overview?lat={db_city.lat}&lon={db_city.lon}&appid={API_KEY}"
    weather_date_res = requests.get(weather_date_url)
    weather_date_data = weather_date_res.json()

    if weather_date_res.status_code != 200:
        return {"Error": "Failed to fetch weather data."}
    
    #save to DB
    new_weather = WeatherDesc(
        city_id=db_city.id,
        date=weather_date_data["date"],
        overview = weather_date_data["weather_overview"],
        )
    
    db.add(new_weather)
    db.commit()
    db.refresh(new_weather)

      #return data
    return{
        "date":weather_date_data["date"],
        "city":db_city.name,
        "country": db_city.country,
        "forecast": weather_date_data["weather_overview"]
    }

