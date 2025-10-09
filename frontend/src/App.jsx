import './App.css';
import WeatherForm from './components/WeatherForm';
import WeatherInfo from './components/WeatherInfo';
import { useState } from 'react';
import axios from "axios";

function App() {

const [cityInfo, setCityInfo] = useState(null);
const [country, setCountry] = useState(null);
console.log(cityInfo, country)

  return (
    <>
    <div className="container">
        <header className="header">
             <h1 className="page-title"> 🌤️ Weather App</h1>
             <WeatherForm setCityInfo={setCityInfo} setcountry={setCountry} />
        </header>
        <main className="main-content">
          
            {cityInfo && country && <WeatherInfo city={cityInfo} country={country} />}

        </main>
    </div>
    </>
        
  );
}

export default App;
