from fastapi import FastAPI, Depends
import os, requests
from dotenv import load_dotenv


load_dotenv()
API_KEY = os.getenv("OPENWEATHER_API_KEY")

app = FastAPI()

@app.get("/geo")
def get_weather(city: str, country: str):
    """Fetch current weather for a given city and country"""

    #Get latitude and longitude
    geo_url = f"http://api.openweathermap.org/geo/1.0/direct?q={city},{country}&appid={API_KEY}"
    geo_resp = requests.get(geo_url)
    geo_data = geo_resp.json()

    if not geo_data:
        return {"error": "City not found. Check spelling or try another city."}

    lat, lon = geo_data[0]["lat"], geo_data[0]["lon"]
    

    #Get current weather
    weather_url = f"https://api.openweathermap.org/data/2.5/weather?lat={lat}&lon={lon}&appid={API_KEY}&units=metric"
    weather_res = requests.get(weather_url)
    weather_data = weather_res.json()

    if weather_res.status_code != 200:
        return {"Error": "Failed to fetch weather data."}
    
    print("weather", weather_data)
    
    #return data
    return{
        "city":city.title(),
        "country": country.upper(),
        "temperature": weather_data["main"]["temp"],
        "feels_like": weather_data["main"]["feels_like"],
        "humidity": weather_data["main"]["humidity"],
        "description": weather_data["weather"][0]["description"],
        "wind_speed": weather_data["wind"]["speed"]
    }

   