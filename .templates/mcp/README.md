# MCP Server Starter Template

A minimal, bare-bones MCP (Model Context Protocol) server template in Python using FastMCP. This template provides a simple starting point that can be easily expanded with additional tools.

## Features

- 🚀 Minimal setup with uv package manager
- 🔧 Three example tools: `hello`, `echo`, and `add_numbers`
- 📝 Clear structure for adding new tools
- 🐍 Python 3.10+ with type hints
- 📦 FastMCP for simple tool definitions

## Setup

The server will run using stdio transport, ready to be connected to by an MCP client.

## Adding New Tools

Adding a new tool is simple - just add a new decorated async function to `server.py`:

```python
@mcp.tool()
async def my_new_tool(param1: str, param2: int) -> str:
    """
    Description of what your tool does.
    
    Args:
        param1: Description of first parameter
        param2: Description of second parameter
    
    Returns:
        Description of what gets returned
    """
    # Your tool implementation here
    result = process_data(param1, param2)
    return f"Processed: {result}"
```

That's it! The tool will be automatically available to MCP clients.

## Project Structure

```
mcp-server-starter/
├── bin/
│   ├── init    # Initialize virtual environment and dependencies
│   ├── run     # Run the MCP server
│   └── uv      # uv wrapper script
├── server.py   # Main server implementation
├── pyproject.toml  # Project dependencies
├── .python-version # Python version specification
└── README.md   # This file
```

## Example Tools

The template includes three simple example tools:

1. **hello** - Greets someone by name
2. **echo** - Returns whatever message is sent to it
3. **add_numbers** - Adds two numbers together

## Testing Your Server

You can test your MCP server using an MCP client. For example, with the MCP CLI:

```bash
# Install MCP CLI (if not already installed)
npm install -g @modelcontextprotocol/cli

# Test your server
mcp-cli ./bin/run
```

## Expanding the Template

To build a production-ready MCP server, consider adding:

- Error handling and validation
- Async HTTP requests (using `httpx`)
- Database connections
- External API integrations
- Logging and monitoring
- Configuration management
- Additional transport options

## Dependencies

- **FastMCP** - Simplified MCP server framework
- **Python 3.10+** - Modern Python with type hints
- **uv** - Fast Python package manager

## License

This is a template - use it however you like!

## Resources

- [Model Context Protocol Documentation](https://modelcontextprotocol.io/)
- [FastMCP Documentation](https://github.com/danielgross/fastmcp)
- [MCP Quickstart Guide](https://modelcontextprotocol.io/docs/quickstart)
