import requests
import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime, timedelta
import os

# 1. Get weather data
today = datetime.now()
week_ago = today - timedelta(days=7)
start_date = week_ago.strftime("%Y-%m-%d")
end_date = today.strftime("%Y-%m-%d")

url = (
    f"https://api.open-meteo.com/v1/forecast"
    f"?latitude=35.09"
    f"&longitude=89.81"
    f"&start_date={start_date}"
    f"&end_date={end_date}"
    f"&daily=temperature_2m_max,temperature_2m_min"
)
response = requests.get(url)
response.raise_for_status()
data = response.json()

# 2. Process with pandas
df = pd.DataFrame({
    "date": pd.to_datetime(data["daily"]["time"]),
    "max_temp_c": data["daily"]["temperature_2m_max"],
    "min_temp_c": data["daily"]["temperature_2m_min"]
})

# 3. Convert Celsius to Fahrenheit
df["max_temp_f"] = (df["max_temp_c"] * 9 / 5) + 32
df["min_temp_f"] = (df["min_temp_c"] * 9 / 5) + 32
df["avg_temp_c"] = (df["max_temp_c"] + df["min_temp_c"]) / 2
df["avg_temp_f"] = (df["avg_temp_c"] * 9 / 5) + 32

# 4. Create visualization
plt.figure(figsize=(11, 6))

# Plot Celsius lines
plt.plot(df["date"], df["max_temp_c"], "r-o", label="Max (°C)")
plt.plot(df["date"], df["min_temp_c"], "b-o", label="Min (°C)")
plt.plot(df["date"], df["avg_temp_c"], "g--", label="Average (°C)")

# Add labels for max and min in both C and F
for _, row in df.iterrows():
    max_label = f"{row['max_temp_c']:.1f}°C / {row['max_temp_f']:.1f}°F"
    min_label = f"{row['min_temp_c']:.1f}°C / {row['min_temp_f']:.1f}°F"

    plt.text(
        row["date"],
        row["max_temp_c"] + 0.6,
        max_label,
        ha="center",
        va="bottom",
        fontsize=8,
        color="red"
    )

    plt.text(
        row["date"],
        row["min_temp_c"] - 0.6,
        min_label,
        ha="center",
        va="top",
        fontsize=8,
        color="blue"
    )

# Format x-axis labels without year, horizontal
date_labels = df["date"].dt.strftime("%b %d")
plt.xticks(df["date"], date_labels, rotation=0)

plt.xlabel("Date")
plt.ylabel("Temperature (°C)")
plt.title("Germantown Weather - Past Week")
plt.legend()
plt.grid(True, alpha=0.3)
plt.tight_layout()

# 5. Save everything
if not os.path.exists("data"):
    os.makedirs("data")

plt.savefig("data/weather_chart.png", dpi=300)
df.to_csv("data/weather.csv", index=False)

# 6. Print summary
print("Daily weather data:")
print(df[["date", "max_temp_c", "min_temp_c", "max_temp_f", "min_temp_f"]])

print(f"\nAverage temperature: {df['avg_temp_c'].mean():.1f}°C / {df['avg_temp_f'].mean():.1f}°F")
print("Files saved in 'data' folder")