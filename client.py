import asyncio
from mcp import ClientSession
from mcp.client.streamable_http import streamable_http_client
from openai import OpenAI
from dotenv import load_dotenv

load_dotenv()  #load environment variables from .env file
client = OpenAI() #initialize OpenAI client

SYSTEM_PROMPT = """
You are an MCP Client with access to external tools.
Once you receive the user's request, check avaiable tools and make
a decision on whether the user's request should be answered via a tool
or via internal data.

"""

def convert_tool(tool):
    return {
        "type": "function",
        "name": tool.name,
        "description": tool.description or "",
        "parameters": tool.inputSchema      
    }
    
async def main():
    # Connect to a streamable HTTP server
    async with streamable_http_client("http://localhost:8001/mcp") as (
        read_stream,
        write_stream,
        _,
    ):
        # Create a session using the client streams
        async with ClientSession(read_stream, write_stream) as session:
            # Initialize the connection
            await session.initialize()
            # List available tools
            tool_list = await session.list_tools()
            print(tool_list.tools) 

asyncio.run(main()) 