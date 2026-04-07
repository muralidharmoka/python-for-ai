import os
import requests
import json
from dotenv import load_dotenv

load_dotenv() 

def get_weather(zipcode):
    apikey = os.getenv("OPEN_WEATHERMAP_API_KEY")
    countrycode="us" # Assuming the country code is US, you can modify it as needed
    URL = f"https://api.openweathermap.org/data/2.5/weather?zip={zipcode},{countrycode}&appid={apikey}"
    result = requests.get(URL)
    response = result.json()
    return response

print(get_weather("38139"))