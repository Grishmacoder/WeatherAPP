import './App.css';
import WeatherForm from './components/WeatherForm';
import WeatherInfo from './components/WeatherInfo';
import { useState } from 'react';
import axios from "axios";
import WeatherOverview from './components/WeatherOverview';

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
             {cityInfo && country && <WeatherOverview city={cityInfo} country={country}/>}
        </header>
        <main className="main-content">
          
            {cityInfo && country && <WeatherInfo city={cityInfo} country={country} />}

           
        </main>
    </div>
    </>
        
  );
}

export default App;
