from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()  #load environment variables from .env file
client = OpenAI() #initialize OpenAI client

f = open("cot.txt", "r")  #open the file containing system prompt and read its content
sys_prompt = f.read()
f.close()

user_input = input("HUMAN INPUT: ") #take user input from Whthe console

#create a response using the OpenAI client with the specified model, system prompt, and user input
response = client.responses.create(
model="gpt-5.4-mini", 
instructions=sys_prompt,
input=user_input
)

print(response.output[0].content[0].text)