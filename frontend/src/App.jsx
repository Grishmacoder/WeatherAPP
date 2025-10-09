import './App.css';
import WeatherForm from './components/WeatherForm';
import WeatherInfo from './components/WeatherInfo';
import { useState } from 'react';
import WeatherOverview from './components/WeatherOverview';
import WeatherByDate from './components/WeatherByDate';

function App() {

const [cityInfo, setCityInfo] = useState(null);
const [country, setCountry] = useState(null);
const [seletedDate, setSelectedDate] = useState(null)

console.log(cityInfo, country, seletedDate)

  return (
    <>
    <div className="container">
        <header className="header">
             <h1 className="page-title"> 🌤️ Weather App</h1>
             <WeatherForm setCityInfo={setCityInfo} setcountry={setCountry} setSelectedDate={setSelectedDate} />
             {cityInfo && country && <WeatherOverview city={cityInfo} country={country}/>}
        </header>
        <main className="main-content">
          
            {cityInfo && country && 
            (seletedDate ? (<WeatherByDate city={cityInfo} country={country} date={seletedDate} />):(<WeatherInfo city={cityInfo} country={country} />))
            }

           
        </main>
    </div>
    </>
        
  );
}

export default App;
