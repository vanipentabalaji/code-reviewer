import os
from mcp.server.fastmcp import FastMCP

mcp = FastMCP("CodeReviewer")

@mcp.tool()
def read_file(file_path: str) -> str:
    """Read the contents of a code file to review it."""
    try:
        abs_path = os.path.abspath(file_path)
        if not os.path.exists(abs_path):
            return f"File not found: {file_path}"
        with open(abs_path, 'r', encoding='utf-8') as file:
            return file.read()
    except Exception as e:
        return f"Error reading file: {str(e)}"


if __name__ == "__main__":
    mcp.run(transport="stdio")