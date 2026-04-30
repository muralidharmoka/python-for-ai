from fastapi import requests
from mcp.server.fastmcp import FastMCP
import requests
import wikipedia

mcp = FastMCP("Support Server", json_response=True,host="127.0.0.1",port=8001)

@mcp.tool()
def wikipedia_search(topic: str):
    """
    GET Wikipedia Summary of any topic by providing the relevant
    topic name. This tool is limited to only providing 10 sentence summary.
    """
    try:
        summary = wikipedia.summary(topic, sentences=10)
        return summary
    except Exception as e:
        return f"An error occurred while fetching the Wikipedia summary: {str(e)}"


@mcp.tool()
def ecommerce_data(product_name: str):
    """
    GET E-commerce data of any product by providing the relevant product name.
    """
    return f"Data for {product_name} is currently unavailable."

@mcp.tool()
def get_order_data(user_id: int):
    """
    GET Order data and delivery information for a user based on 
    their user ID."""
    url = f"http://localhost:8000/delivery_status/{user_id}"
    response = requests.get(url)
    if response.status_code != 200:
        return {"error": f"Failed to fetch data for user ID {user_id}. Status code: {response.status_code}"}
    return response.json()


if __name__ == "__main__":
    print("MCP server started. Waiting for client...")
    mcp.run(transport="streamable-http")