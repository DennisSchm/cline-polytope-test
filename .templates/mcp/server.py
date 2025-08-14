#!/usr/bin/env python3
"""
Minimal MCP Server Starter Template
A bare-bones hello world MCP server that can be easily expanded.
"""

from typing import Any
from fastmcp import FastMCP

# Initialize the MCP server
mcp = FastMCP("mcp-starter")


@mcp.tool()
async def hello(name: str = "World") -> str:
    """
    A simple hello tool that greets someone by name.

    Args:
        name: The name to greet (defaults to "World")

    Returns:
        A greeting message
    """
    return f"Hello, {name}!"


@mcp.tool()
async def echo(message: str) -> str:
    """
    Echoes back whatever message is sent to it.

    Args:
        message: The message to echo back

    Returns:
        The same message that was sent
    """
    return message


@mcp.tool()
async def add_numbers(a: float, b: float) -> str:
    """
    Adds two numbers together.

    Args:
        a: First number
        b: Second number

    Returns:
        The sum of a and b
    """
    result = a + b
    return f"The sum of {a} and {b} is {result}"


# Example of how to add a new tool:
# @mcp.tool()
# async def my_new_tool(param1: str, param2: int) -> str:
#     """
#     Description of what your tool does.
#
#     Args:
#         param1: Description of first parameter
#         param2: Description of second parameter
#
#     Returns:
#         Description of what gets returned
#     """
#     # Your tool implementation here
#     return f"Result based on {param1} and {param2}"


if __name__ == "__main__":
    # Run the server using stdio transport
    mcp.run(transport="http", host="0.0.0.0", port=3030)
