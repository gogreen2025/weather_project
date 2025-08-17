import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

# Load the daily summary CSV 
data_dir = Path(__file__).parent.parent / "data"
daily_csv_path = data_dir / "weather_forecast_daily.csv"
if not daily_csv_path.exists():
    raise FileNotFoundError(f"{daily_csv_path} not found. Please run scrape_weather.py first.")

daily_df = pd.read_csv(daily_csv_path)

#Ensure date column is datetime type
daily_df["date"] = pd.to_datetime(daily_df["date"])

#Sort by city and date
daily_df = daily_df.sort_values(by=["city", "date"])

# Create plots directory if not exists
plots_dir = Path(__file__).parent.parent / "plots"
plots_dir.mkdir(exist_ok=True)

# Preview data
print(daily_df.head())  
# Plot daily average temperature for each city
plt.figure(figsize=(12, 6))
for city in daily_df["city"].unique():
    city_data = daily_df[daily_df["city"] == city]
    plt.plot(city_data["date"], city_data["temp"], marker='o', label=city)
plt.title("Daily Average Temperature Forecast")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
# Save plot
plot_path = data_dir / "daily_avg_temperature.png"
plt.savefig(plot_path)
print(f"Saved plot to {plot_path}")
plt.show()

#2. High and Low Temperatures
plt.figure(figsize=(12, 6))
for city in daily_df["city"].unique():
    city_data = daily_df[daily_df["city"] == city]
    plt.plot(city_data["date"], city_data["temp_max"], marker='^', linestyle='--', label=f"{city} Max")
    plt.plot(city_data["date"], city_data["temp_min"], marker='v', linestyle=':', label=f"{city} Min")
plt.title("Daily High and Low Temperature Forecast")
plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.xticks(rotation=45)
plt.legend()
plt.tight_layout()
# Save plot
plot_path = data_dir / "daily_high_low_temperature.png"
plt.savefig(plot_path)
print(f"Saved plot to {plot_path}")
plt.show()  


