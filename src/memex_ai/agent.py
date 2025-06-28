# src/memex_ai/agent.py
import sqlite3

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.sqlite import SqliteSaver
from langgraph.store.memory import InMemoryStore
from langmem import create_manage_memory_tool, create_search_memory_tool

from .config import OPENAI_API_KEY
from .tools.web_scraper import scrape_url


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

    system_prompt = """You are Memex, a personalized AI research assistant. Your
    primary goal is to help users with research by remembering key facts and context
    across conversations.

    **Your Capabilities:**
    1.  **Web Scraping:** You can use the `scrape_url` tool to get content from
    websites.
    2.  **Memory Management:** You have a memory system.

    **How to Use Your Memory (VERY IMPORTANT):**
    -   **Storing Facts:** When the user provides an important fact to remember, you
    MUST use the `manage_memory` tool to save it. After using the tool successfully,
    you should confirm this action to the user.
    -   **Recalling Facts:** When the user asks a question, first consider if it might
    relate to a stored fact. If so, use the `search_memory` tool to find the
    information before answering.
    """

    agent_executor = create_react_agent(
        model,
        tools=tools,
        prompt=system_prompt,
        checkpointer=checkpointer,
    )

    print(
        """✅ Memex AI Agent with persistent history and in-memory tools
created successfully."""
    )
    return agent_executor
