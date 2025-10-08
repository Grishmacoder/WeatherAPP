import { useState } from "react";
import PropTypes from "prop-types";
import "./WeatherForm.css";

function WeatherForm({ onSubmit }) {
  const [location, setLocation] = useState("");
  const handleSubmit = (e) => {
    e.preventDefault();
    onSubmit(location);
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
