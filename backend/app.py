from fastapi import FastAPI, Depends
import os, requests
from dotenv import load_dotenv
from datetime import datetime

from sqlalchemy.orm import Session
from database import SessionLocal, engine
from models import City,WeatherDesc, Base


#create table if not exist
Base.metadata.create_all(bind=engine)

#load env
load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = FastAPI()

#get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@app.post("/city")
def get_weather(city: str, country: str, db: Session = Depends(get_db)):
    """Fetch current weather for a given city and country"""

    #Get latitude and longitude
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{country}&appid={API_KEY}"
    geo_resp = requests.get(geo_url)
    geo_data = geo_resp.json()

    if not geo_data:
        return {"error": "City not found. Check spelling or try another city."}

    lat, lon = geo_data[0]["lat"], geo_data[0]["lon"]

    #check if city alredy exsists
    db_city = db.query(City).filter(City.name == city, City.country == country).first()
    if db_city:
        return {"message": "City already exists", "city": db_city.name, "lat": db_city.lat, "lon": db_city.lon}

    new_city = City(name=city, country=country, lat=lat, lon=lon)
    db.add(new_city)
    db.commit()
    db.refresh(new_city)
    return {"message": "City added successfully", "city": city, "lat": lat, "lon": lon}
    
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
    return{
        "city":db_city.name,
        "country": db_city.country,
        "temperature": weather_data["main"]["temp"],
        "feels_like": weather_data["main"]["feels_like"],
        "humidity": weather_data["main"]["humidity"],
        "description": weather_data["weather"][0]["description"],
        "wind_speed": weather_data["wind"]["speed"]
    }

   