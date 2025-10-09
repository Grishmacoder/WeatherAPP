import React from 'react'
import { useEffect, useState } from "react";
import axios from "axios";
import  "./WeatherInfo.css";

function WeatherInfo({city, country}) {
    const [weather, setweather] = useState(null);

    useEffect(() => {
      if(!city || !country) return;
    
      const fetchWeather= async() => {
        try{
            const res = await axios.get(
                `http://127.0.0.1:8000/weather?city=${encodeURIComponent(city)}&country=${encodeURIComponent(country)}`
            );
            setweather(res.data);
            console.log("i'm called in weahter info", res.data);
        }catch(err){
            console.error("Error fetching weather: ",err);
        }
      };
      fetchWeather();
    }, [city, country]);

    if(!weather) return <p>Loading weather data...</p>;
    if(weather.error) return <p>{weather.error}</p>;
    
  return (
       <article className="weathercard">
      <div className="weathercard__container">
        <div className="weathercard__meta"></div>
        <div className="weathercard__details">
          <span className="weathercard__location">
            {weather.city} ,{weather.country}
          </span>
        </div>
        <div className="weathercard__temp">
          <span className="weathercard__temperature">
             🌡{weather.temperature}°C
          </span>
        </div>

        <div className="weathercard__wind">
          <div className="weathercard__wind-direction">
            <span
              className="weathercard__wind-direction-arrow"
              style={{ transform: `rotate(${weather.wind_speed + 90}deg)` }}
            >
              &#8599; {weather.wind_speed}°
            </span>
        
          </div>
          <div className="weathercard__wind-speed-container">
            <span className="weathercard__wind-speed">
              Wind: {weather.wind_speed}{"m/s"}
            </span>
          </div>
        </div>
        <div className="weathercard__humidity">
          💧 Humidity: {weather.humidity}%
        </div>
        <div className="weathercard_description">
          <span className="weathercard__description-text">
            {weather.description}
          </span>
        </div>
        {/* <div className="weathercard__units-toggle">
          <button onClick={() => setUnits("metric")}>°C</button>
          <button onClick={() => setUnits("imperial")}>°F</button>
        </div> */}
      </div>
    </article>
  )
}

export default WeatherInfo