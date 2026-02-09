from fastmcp import FastMCP
from datetime import datetime

mcp=FastMCP(name="fileformet",instructions="This server help to convert data to file txt format")

@mcp.tool()
def save_text_to_file(data: str, filename: str = "research_output.txt") -> str:
    """Saves structured research data to a text file."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    formatted_text = f"--- Research Output ---\nTimestamp: {timestamp}\n\n{data}\n\n"

    with open(filename, "a", encoding="utf-8") as f:
        f.write(formatted_text)

    return f"Data successfully saved to {filename}"


if __name__=="__main__":
    mcp.run(transport="stdio")