import './App.css';
import WeatherForm from './components/WeatherForm';
import { useState } from 'react';
import axios from "axios";

function App() {

const [cityInfo, setCityInfo] = useState(null);


    // Function to add city to the backend
const handleFormSubmit = async (location) => {
    try {
      const parts = location.split(",").map((p) => p.trim());
      const city = parts[0];
      const country = parts[parts.length - 1];
      console.log(city, country)

      const response = await axios.post(`http://127.0.0.1:8000/city?city=${encodeURIComponent(city)}&country=${encodeURIComponent(country)}`);

      setCityInfo(response.data);
      console.log(response);
      alert(`City ${response.data.city} added successfully!`);
    } catch (error) {
      console.error("Error adding city:", error);
      alert("Failed to add city");
    }
  };

  return (
    <>
    <div className="container">
        <header className="header">
             <h1 className="page-title">Weather App</h1>
             <WeatherForm onSubmit={handleFormSubmit} />
              
        </header>
    </div>
    </>
        
  );
}

export default App;
