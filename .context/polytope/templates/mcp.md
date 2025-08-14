<instructions>
<title>Documentation on how to create MCP (Model Context Protocol) servers using Polytope</title>

<mcp_server_overview>
<section_title>MCP Server Starter Template</section_title>
A minimal, bare-bones MCP (Model Context Protocol) server template in Python using FastMCP. This template provides a simple starting point that can be easily expanded with additional tools.

<features>
- 🚀 Minimal setup with uv package manager
- 🔧 Three example tools: `hello`, `echo`, and `add_numbers`
- 📝 Clear structure for adding new tools
- 🐍 Python 3.10+ with type hints
- 📦 FastMCP for simple tool definitions
- 🔍 MCP Inspector for debugging and testing
</features>

The server runs using stdio transport, ready to be connected to by an MCP client.
</mcp_server_overview>

<component_creation>
<section_title>Creating MCP Server Components</section_title>
Use the mcp template to automatically generate pre-configured MCP server components. This eliminates the need to manually configure MCP modules and provides a complete starter template.

<generate_component>
<subsection_title>Generate an MCP Server Component</subsection_title>
Execute the following command in the terminal to use the polytope scaffold command with the mcp template:
`pt run --raw "polytope/scaffold{template: '.templates/mcp', path: 'mcp-server'}"`

<examples>
<example_title>Examples</example_title>

Basic MCP server component:
`pt run --raw "polytope/scaffold{template: '.templates/mcp', path: 'mcp-server'}"`

Weather MCP server:
`pt run --raw "polytope/scaffold{template: '.templates/mcp', path: 'weather-mcp'}"`

Database MCP server:
`pt run --raw "polytope/scaffold{template: '.templates/mcp', path: 'db-mcp'}"`
</examples>

<generated_features>
The generated component includes:
- Pre-configured `polytope.yml` file with Python module setup
- Complete MCP server implementation in `server.py`
- Project dependencies in `pyproject.toml`
- Executable scripts in `bin/` directory (init, run, uv)
- MCP Inspector for debugging and testing tools
- Three example tools ready to use

**IMPORTANT:** The generated `polytope.yml` file is pre-configured for MCP server development and should not be modified unless you need to change the server configuration or add additional services.
</generated_features>
</generate_component>
</component_creation>

<package_management>
<section_title>Adding Python Packages to MCP Server Components</section_title>
Each MCP server component created with the template includes a custom `{component-name}-add` module for adding Python packages to the pyproject.toml file.

**IMPORTANT**: Make sure to ALWWAYS add dependencies before running the component. The add module is only available AFTER the component has been generated and the main polytope.yml includes the component's polytope.yml file.

<usage>
**Usage:**
Execute the following command in the terminal to add Python packages to your MCP server.

`pt run --raw "{component-name}-add{packages: 'package-name'}"`
</usage>

<package_examples>
<subsection_title>Examples</subsection_title>
Execute the following command in the terminal to add packages to your MCP server.

For an 'mcp-server' component:
`pt run --raw "mcp-server-add{packages: 'httpx'}"`

For a 'weather-mcp' component:
`pt run --raw "weather-mcp-add{packages: 'requests'}"`

Multiple packages:
`pt run --raw "mcp-server-add{packages: 'httpx sqlalchemy pydantic'}"`

Database-related packages:
`pt run --raw "mcp-server-add{packages: 'asyncpg psycopg2-binary'}"`
</package_examples>

<package_guidelines>
**IMPORTANT:** 
- Do NOT specify package versions unless specifically requested by the user
- Use space-separated package names for multiple packages
- The packages parameter accepts comma or whitespace-separated lists
- Common useful packages for MCP servers include: httpx, requests, sqlalchemy, pydantic, asyncpg, redis, etc.
</package_guidelines>
</package_management>

<adding_tools>
<section_title>Adding New MCP Tools</section_title>
Adding a new tool to your MCP server is simple - just add a new decorated async function to `server.py`:

<tool_example>
<code language="python">
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
</code>

That's it! The tool will be automatically available to MCP clients.
</tool_example>
</adding_tools>

<project_structure>
<section_title>MCP Server Project Structure</section_title>
The generated MCP server follows this structure:

```
mcp-server/
├── bin/
│   ├── init    # Initialize virtual environment and dependencies
│   ├── run     # Run the MCP server
│   └── uv      # uv wrapper script
├── server.py   # Main server implementation with tools
├── pyproject.toml  # Project dependencies
├── .python-version # Python version specification
├── polytope.yml    # Polytope configuration
└── README.md   # Documentation
```
</project_structure>

<example_tools>
<section_title>Included Example Tools</section_title>
The template includes three simple example tools to get you started:

1. **hello** - Greets someone by name
2. **echo** - Returns whatever message is sent to it  
3. **add_numbers** - Adds two numbers together

These tools demonstrate different parameter types and return patterns you can use as templates for your own tools.
</example_tools>

<testing_server>
<section_title>Testing Your MCP Server</section_title>
The template includes multiple ways to test your MCP server:

<mcp_inspector>
<subsection_title>Using MCP Inspector</subsection_title>
The generated component includes MCP Inspector for visual debugging:
1. Start your MCP server: `pt run mcp-server`
2. Start MCP Inspector: `pt run mcp-inspector`  
3. Open http://localhost:6274 in your browser
4. Connect to your MCP server and test tools interactively
</mcp_inspector>
</testing_server>

<expanding_template>
<section_title>Expanding the Template</section_title>
To build a production-ready MCP server, consider adding:

- Error handling and validation
- Async HTTP requests (using `httpx`)
- Database connections
- External API integrations
- Logging and monitoring
- Configuration management
- Additional transport options
- Resource providers (not just tools)

The FastMCP framework makes it easy to add these capabilities incrementally.
</expanding_template>

<dependencies>
<section_title>Key Dependencies</section_title>
- **FastMCP** - Simplified MCP server framework
- **Python 3.10+** - Modern Python with type hints
- **uv** - Fast Python package manager
- **MCP Inspector** - Visual debugging and testing tool

All dependencies are automatically managed through the generated `pyproject.toml` file.
</dependencies>
</instructions>
