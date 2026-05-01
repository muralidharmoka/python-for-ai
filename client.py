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

def convert_tools(tool):
    return {
        "type": "function",
        "name": tool.name,
        "description": tool.description or "",
        "parameters": tool.inputSchema      
    }
    
#Main MCP Client function
async def main():
    query = input("Enter your query: ")
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
            openai_tools = [convert_tools(t) for t in tool_list.tools]
            #print("Available tools:", openai_tools)

            response = client.responses.create(
                model="gpt-5.4-mini",
                instructions=SYSTEM_PROMPT,
                input=query,
                tools=openai_tools,
            )

            tool_call = None
            for item in response.output:
                if item.type == "function_call":
                    tool_call = item
                    break
            if tool_call:
                tool_name = tool_call.name
                args = tool_call.arguments
                print(f"Calling tool: {tool_name} with arguments: {args}")
                

asyncio.run(main()) 