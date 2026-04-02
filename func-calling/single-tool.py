from openai import OpenAI
from dotenv import load_dotenv
import requests
import os   
import json
load_dotenv()  #load environment variables from .env file
client = OpenAI() #initialize OpenAI client     
# Define a function to get weather information using OpenWeatherMap API
#create our AI Tool

def get_weather(zipcode):
    apikey = os.getenv("OPEN_WEATHERMAP_API_KEY")
    countrycode="us" # Assuming the country code is US, you can modify it as needed
    URL = f"https://api.openweathermap.org/data/2.5/weather?zip={zipcode},{countrycode}&appid={apikey}"
    result = requests.get(URL)
    response = result.json()
    return response

tools = [
    {
        "type": "function",
        "name": "get_weather",
        "description": "Get weather information for a given zipcode.",
        "parameters": {
            "type": "object",
            "properties": {
                "zipcode": {
                    "type": "string",
                    "description": "Any string that represents the zipcode for which you want to get the weather information.",
                },
            },
            "required": ["zipcode"],
        },
    },
]

#First LLM Call
user_input = input("HUMAN INPUT: ")
response = client.responses.create(
    model="gpt-5.4-mini",
    input=user_input,
    tools=tools,
)

for item in response.output:
    if item.type == "function_call":
        arguments = json.loads(item.arguments)

        if item.name == "get_weather":
            weather_info = get_weather(arguments["zipcode"])
            print("Weather Information: ", weather_info)