from fastapi import requests
from mcp.server.fastmcp import FastMCP
import requests
import wikipedia

mcp = FastMCP("Support Server", json_response=True,host="127.0.0.1",port=8001)

# This tool is designed to fetch a summary of a given topic from Wikipedia.
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

# This tool is designed to fetch e-commerce data for a given product name.
@mcp.tool()
def ecommerce_data(product_name: str):
    """
    GET E-commerce data of any product by providing the relevant product name.
    """
    return f"Data for {product_name} is currently unavailable."

# This tool is designed to fetch order and delivery information for a user based on their user ID.
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

@mcp.tool()
def get_internal_data(message: str):
    """
    Tool to query the internal database of the Company.
    It connectes to the database, searches the database for a given topic,
    and provides the relevant matches related to that topic.
    """
    return {
        "status":"completed",
        "data":"this is some fake data"
    }

if __name__ == "__main__":
    print("MCP server started. Waiting for client...")
    mcp.run(transport="streamable-http")