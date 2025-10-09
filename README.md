# 🌤 Weather App

A full-stack Weather Application that fetches real-time weather data using the OpenWeather API.  
The project consists of a **React.js frontend** and a **FastAPI backend**, with **PostgreSQL** used as the database.

---


## ⚙️ Prerequisites

Before you begin, make sure you have the following installed:

- [Node.js](https://nodejs.org/) (v16 or above)
- [Python](https://www.python.org/) (v3.8 or above)
- [PostgreSQL](https://www.postgresql.org/download/)
- [Git](https://git-scm.com/)

## 🚀 Setup Instructions

### 1️⃣ Clone the Repository

```bash
git clone https://github.com/Grishmacoder/WeatherAPP.git
cd WeatherAPP
```

### 2️⃣ Backend Setup (FastAPI)
📦 Install Dependencies
```
cd backend
pip install -r requirements.txt
```
🗄️ Setup PostgreSQL Database

Ensure PostgreSQL is running locally.
Create a new database (e.g., weather_db).
Update your database URL and openWeather API Key in .env:

```bash
uvicorn app:app --reload
```
By default, the server runs at:
👉 http://127.0.0.1:8000

### 3️⃣ Frontend Setup (React)
📦 Install Dependencies
```
cd ../frontend
npm install 
```
▶️ Run the Frontend
```
npm start
```
The React app will start on:
👉 http://localhost:3000

🔗 API Connection

The frontend communicates with the backend via REST API endpoints exposed by FastAPI and integrate OpenWeatherAPI.

Ensure both the frontend and backend are running simultaneously.

🧠 Environment Variables

Create a .env file in your backend/ directory and include:
```
OPENWEATHER_API_KEY=your_api_key_here
DATABASE_URL=postgresql://<username>:<password>@localhost:5432/weather_db
```

💡 Notes

Make sure the backend URL is correctly set in your frontend API calls (e.g., http://127.0.0.1:8000).

If PostgreSQL is not running, the backend will fail to connect to the database.

You can change ports or environment variables as needed.