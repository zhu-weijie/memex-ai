# src/memex_ai/tools/meta_tools.py
from langchain_core.tools import tool, BaseTool


def create_list_tools_tool(all_tools: list[BaseTool]) -> BaseTool:
    """A factory that creates the list_tools tool, giving it context."""

    @tool
    def list_tools() -> str:
        """
        Lists the names and descriptions of all available tools, except for this one.
        Use this to tell the user what you are capable of.
        """
        if not all_tools:
            return "I currently have no tools available."

        formatted_tools = []
        for t in all_tools:
            formatted_tools.append(f"- **{t.name}**: {t.description}")

        return "Here are the tools I have available:\n" + "\n".join(formatted_tools)

    return list_tools
