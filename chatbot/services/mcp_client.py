import asyncio
from typing import Dict, Any, Tuple
from mcp.client.stdio import stdio_client, StdioServerParameters
from mcp.client.session import ClientSession
import os

async def call_mcp_tool(tool_name: str, arguments: Dict[str, Any]) -> str:
    """
    Connects to the FastMCP server via stdio, calls the requested tool, and returns the result.
    """
    base_dir = os.path.dirname(os.path.dirname(os.path.dirname(__file__)))
    server_path = os.path.join(base_dir, "mcp_server", "server.py")
    
    server_parameters = StdioServerParameters(
        command="python",
        args=[server_path]
    )

    try:
        async with stdio_client(server_parameters) as (read, write):
            async with ClientSession(read, write) as session:
                await session.initialize()
                
                # Call the requested tool
                result = await session.call_tool(tool_name, arguments)
                
                # The result is a list of ToolContent objects (usually TextContent)
                if result.content and len(result.content) > 0:
                    return result.content[0].text
                return "Tool returned no output."
    except Exception as e:
        return f"Error communicating with MCP server: {str(e)}"
