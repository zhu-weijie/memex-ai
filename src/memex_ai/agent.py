# src/memex_ai/agent.py
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.memory import InMemorySaver
from langgraph.store.memory import InMemoryStore
from langmem import create_manage_memory_tool, create_search_memory_tool

from .config import OPENAI_API_KEY
from .tools.web_scraper import scrape_url


def create_agent():
    """
    Creates and returns a new LangGraph agent equipped with tools and memory.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set. Please check your .env file.")

    model = ChatOpenAI(model="gpt-4-turbo", temperature=0)

    store = InMemoryStore()

    manage_memory = create_manage_memory_tool(namespace=("user",), store=store)
    search_memory = create_search_memory_tool(namespace=("user",), store=store)

    system_prompt = """You are Memex, a personalized AI research assistant. Your
    primary goal is to help users with research by remembering key facts and context
    across conversations.

    **Your Capabilities:**
    1.  **Web Scraping:** You can use the `scrape_url` tool to get content from
    websites.
    2.  **Memory Management:** You have a memory system to provide personalization.

    **How to Use Your Memory (VERY IMPORTANT):**
    -   **Storing Facts:** When the user tells you an important fact, preference, or
    instruction you should remember, use the `manage_memory` tool. Be specific. For
    example: `manage_memory(content="The user's primary research topic is 'the impact
    of AI on climate change'")`.
    -   **Recalling Facts:** Before you answer *any* question, you should first use the
    `search_memory` tool to see if you already know something relevant. This helps you
    recall past conversations. For example, if the user asks "what's my research
    topic?", use `search_memory(query="user's research topic")`.
    
    Always prioritize using your memory to provide contextually-aware and personalized
    responses.
    """

    tools = [scrape_url, manage_memory, search_memory]

    checkpointer = InMemorySaver()

    agent_executor = create_react_agent(
        model, tools=tools, prompt=system_prompt, checkpointer=checkpointer, store=store
    )

    print("✅ Memex AI Agent with Memory created successfully.")
    return agent_executor
