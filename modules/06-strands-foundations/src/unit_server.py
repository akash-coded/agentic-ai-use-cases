
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("unit-converter")

@mcp.tool(description="Convert kilometers to miles.")
def km_to_miles(km: float) -> float:
    return round(km * 0.621371, 4)

@mcp.tool(description="Convert miles to kilometers.")
def miles_to_km(miles: float) -> float:
    return round(miles / 0.621371, 4)

if __name__ == "__main__":
    mcp.run(transport="stdio")
