from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI()
user_input = input("HUMAN INPUT: ")
response = client.responses.create(
model="gpt-5.4-mini", 
instructions="You are a coding assistant that can only answer question related to Linux and Devops .",
input=user_input
)
print(response.output[0].content[0].text)