# src/memex_ai/tools/meta_tools.py
from langchain_core.tools import tool, BaseTool


@tool
def list_tools(tools: list[BaseTool]) -> str:
    """
    Lists the names and descriptions of all available tools.
    Use this to tell the user what you are capable of.
    """
    if not tools:
        return "I currently have no tools available."

    formatted_tools = []
    for t in tools:
        if t.name != "list_tools":
            formatted_tools.append(f"- **{t.name}**: {t.description}")

    return "Here are the tools I have available:\n" + "\n".join(formatted_tools)
