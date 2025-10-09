import React from 'react'
import { useState, useEffect } from 'react';
import axios from 'axios';
import  "./WeatherOverview.css";

function WeatherOverview({city, country}) {
    const [description, setDescription] = useState(null);

    useEffect(() => {
      if(!city || !country) return;
    
      const fetchWeather= async() => {
        try{
            const res = await axios.get(
                `http://127.0.0.1:8000/weather/overview?city=${encodeURIComponent(city)}&country=${encodeURIComponent(country)}`
            );
            setDescription(res.data);
            
            console.log("i'm called in weahter desc", res.data);
        }catch(err){
            console.error("Error fetching weather: ",err);
        }
      };
      fetchWeather();
    }, [city, country]);

    if(!description) return <p>Loading weather description...</p>;
    if(description.error) return <p>{description.error}</p>;
  return (
    <div className="description">
      <h2 className="description__title">Description</h2>
      <div className="description__divider">
        <h3 className='weather-date'>{description.date}</h3>
      <p className="weather-location">{city}, {country} </p>
      <p className="weather-forecast">{description.forecast}</p>
    </div>
    </div>
  )
}

export default WeatherOverview