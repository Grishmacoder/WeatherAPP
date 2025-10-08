import './App.css';
import WeatherForm from './components/WeatherForm';

function App() {
const handleFormSubmit = () => {
    console.log("on submit");
   
  };

  return (
    <>
    <div className="container">
        <header className="header">
             <h1 className="page-title">Current Weather</h1>
             <WeatherForm onSubmit={handleFormSubmit} />
        </header>
    </div>
    </>
        
  );
}

export default App;
