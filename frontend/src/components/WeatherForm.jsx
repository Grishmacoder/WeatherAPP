import { useState } from "react";
import PropTypes from "prop-types";
import "./WeatherForm.css";
import axios from "axios";


function WeatherForm({ setCityInfo, setcountry }) {
  const [location, setLocation] = useState("");
  const [createdAt, setCreatedAt] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();
   try {
      const parts = location.split(",").map((p) => p.trim());
      const city = parts[0];
      const country = parts[parts.length - 1];

      // if user provided datetime, convert to ISO string, else use current time
      const created_at = createdAt
        ? new Date(createdAt).toISOString()
        : new Date().toISOString();

      const response = await axios.post(
      "http://127.0.0.1:8000/city",{
        city,
        country,
        created_at
        });

      setCityInfo(city);
      setcountry(country);
      console.log(response.data);

      alert(`City ${response.data.city} added successfully!`);
    } catch (error) {
      console.error("Error adding city:", error);
      alert("Failed to add city");
    }

  };

  return (
    <form className="form-container" onSubmit={handleSubmit}>
      <label className="form-label" htmlFor="location">Location:</label>
      <input
        type="text"
        id="location"
        name="location"
        value={location}
        onChange={(e) => setLocation(e.target.value)}
        placeholder="City, state code, country code"
        className="form-input"
      />
      <label style={{ marginLeft: "10px" }}>
        Select Date & Time:
        <input
          type="datetime-local"
          value={createdAt}
          onChange={(e) => setCreatedAt(e.target.value)}
          style={{ marginLeft: "5px" }}
        />
      </label>
      <button type="submit" className="submit-btn">Get Weather</button>
     
      <p className="instructions">
        For USA, enter &quot;city,two-letter state code,US&quot; eg
        &quot;Oskaloosa,IA,US&quot;. For every other country, enter
        &quot;city,two-letter country code&quot; eg. &quot;Lillehammer,NO&quot;.
      </p>
    </form>
  );
}
WeatherForm.propTypes = {
  onSubmit: PropTypes.func,
};
export default WeatherForm;
