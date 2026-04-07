from openai import OpenAI
from dotenv import load_dotenv
import requests
import os   
import json
load_dotenv()  #load environment variables from .env file
client = OpenAI() #initialize OpenAI client     
# Define a function to get weather information using OpenWeatherMap API
#create our AI Tool
import subprocess

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
    {
        "type": "function",
        "name": "run_shell",
        "description": "Run a shell command and get the output.",
        "parameters": {
            "type": "object",
            "properties": {
                "command": {
                    "type": "string",
                    "description": "The shell command to execute.",
                },
            },
            "required": ["command"],
        },
    }
]

#First LLM Call
user_input = input("HUMAN INPUT: ")
#user_input = "What is the weather in Germantown with zip code? 38139" #user input that will be fed to the first LLM call. The LLM will decide which tool to call based on the user input and the tools provided.
response = client.responses.create(
    model="gpt-5.4",
    input=user_input,
    tools=tools,
)

#second LLM Call
def run_shell(command):
    result = subprocess.run(command, shell=True, capture_output=True, text=True)
    return {
    "command": command,
    "stdout": result.stdout.strip(),
    "stderr": result.stderr.strip(),
    "returncode": result.returncode
    }
tool_output = []

for item in response.output:
    if item.type == "function_call":
        arguments = json.loads(item.arguments)

        if item.name == "get_weather":
            result = get_weather(arguments["zipcode"])
            #print("Weather Information: ", weather_info
        elif item.name == "run_shell":
            result = run_shell(arguments["command"])

        else:
            result = "Unknown Tool executed"
        #get the output of the tool and append it to the tool_output list
        tool_output.append({
            "type": "function_call_output",
            "call_id": item.call_id,
            "output": json.dumps(result),
        })

#Second LLM Call is fed with the output of the tool and the previous response id to maintain the context of the conversation. The final response will be generated based on the tool output and the previous response.
final_response = client.responses.create(
    model="gpt-5.4-mini",
    input=tool_output,
    previous_response_id=response.id
)

print("FINAL RESPONSE: ", final_response.output_text)