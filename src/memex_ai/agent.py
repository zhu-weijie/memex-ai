# src/memex_ai/agent.py
import sqlite3
import os

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.store.memory import InMemoryStore
from langmem import create_manage_memory_tool, create_search_memory_tool

from .config import OPENAI_API_KEY, get_project_root
from .tools.web_scraper import scrape_url


def load_prompt_from_file() -> str:
    """Loads the system prompt from the prompts/system_prompt.txt file."""
    prompt_path = os.path.join(get_project_root(), "prompts", "system_prompt.txt")
    try:
        with open(prompt_path, "r", encoding="utf-8") as f:
            return f.read()
    except FileNotFoundError:
        print(f"Error: Could not find prompt file at {prompt_path}")
        return "You are a helpful assistant."


def create_agent():
    """
    Creates a stable agent with a persistent checkpointer for chat history
    and a separate in-memory store for factual memory to prevent deadlocks.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set. Please check your .env file.")

    model = ChatOpenAI(model="gpt-4-turbo", temperature=0)

    memory_store = InMemoryStore()

    conn = sqlite3.connect("memory.sqlite", check_same_thread=False)
    checkpointer = SqliteSaver(conn=conn)

    manage_memory = create_manage_memory_tool(namespace=("user",), store=memory_store)
    search_memory = create_search_memory_tool(namespace=("user",), store=memory_store)

    tools = [scrape_url, manage_memory, search_memory]

    system_prompt = load_prompt_from_file()

    agent_executor = create_react_agent(
        model,
        tools=tools,
        prompt=system_prompt,
        checkpointer=checkpointer,
    )

    print("✅ Memex AI Agent (with external prompt) created successfully.")
    return agent_executor
