import requests
import pandas as pd
from datetime import datetime, UTC 
import os
from dotenv import load_dotenv
from pathlib import Path


# Force load .env from project root
env_path = Path(__file__).parent.parent / ".env"
load_dotenv(dotenv_path=env_path)

API_KEY = os.getenv("API_KEY")
print(f"DEBUG: API key loaded? {API_KEY is not None}")  # Should print True


test_url = f"http://api.openweathermap.org/data/2.5/weather?q=London&appid={API_KEY}&units=metric"
test_resp = requests.get(test_url)
print(test_resp.status_code, test_resp.text)


# --- City list ---
cities = ["London", "New York", "Tokyo"]


all_data = []

for city in cities:
    url = f"http://api.openweathermap.org/data/2.5/forecast"
    params = {
        "q": city,
        "appid": API_KEY,
        "units": "metric"
    }
    
    response = requests.get(url, params=params)
    if response.status_code != 200:
        print(f"Error fetching {city}: {response.text}")
        continue

    data = response.json()

    # Loop through every 3-hour forecast 
    for entry in data["list"]:
        dt = datetime.fromtimestamp(entry["dt"], UTC)
        date_str = dt.strftime("%Y-%m-%d %H:%M:%S")
        all_data.append({
            "city": city,
            "date": date_str,
            "datetime": entry["dt_txt"],
            "temp": entry["main"]["temp"],
            "temp_min": entry["main"]["temp_min"],
            "temp_max": entry["main"]["temp_max"],
            "humidity": entry["main"]["humidity"],
            "weather": entry["weather"][0]["description"]
        })

# Create DataFrame
df = pd.DataFrame(all_data)

if not df.empty:
    daily_df = (
        df.groupby(["city", "date"])
          .agg({
              "temp": "mean",
              "temp_min": "min",
              "temp_max": "max",
              "humidity": "mean"
          })
          .reset_index()
    )

    # --- Absolute path to /data folder in project root ---
    data_dir = Path(__file__).parent.parent / "data"
    data_dir.mkdir(exist_ok=True)

    df.to_csv(data_dir / "weather_forecast_3h.csv", index=False)
    daily_df.to_csv(data_dir / "weather_forecast_daily.csv", index=False)

    print("Saved:")
    print(f" - 3-hour forecast -> {data_dir / 'weather_forecast_3h.csv'}")
    print(f" - Daily summary   -> {data_dir / 'weather_forecast_daily.csv'}")
    print(daily_df.head())
else:
    print("No data retrieved. CSVs not created.")