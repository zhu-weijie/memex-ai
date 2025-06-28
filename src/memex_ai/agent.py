# src/memex_ai/agent.py
import sqlite3

from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent
from langgraph.checkpoint.sqlite import SqliteSaver

from .config import OPENAI_API_KEY
from .tools.web_scraper import scrape_url


def create_agent():
    """
    Creates and returns a new LangGraph agent with a persistent
    conversation history checkpointer.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set. Please check your .env file.")

    model = ChatOpenAI(model="gpt-4-turbo", temperature=0)
    tools = [scrape_url]

    conn = sqlite3.connect("memory.sqlite", check_same_thread=False)

    checkpointer = SqliteSaver(conn=conn)

    system_prompt = """You are a helpful assistant. You have access to a tool for
    scraping web pages.
    - `scrape_url`: Use this tool to get the contents of a webpage.
    """

    agent_executor = create_react_agent(
        model, tools=tools, prompt=system_prompt, checkpointer=checkpointer
    )

    print("✅ Memex AI Agent with PERSISTENT HISTORY created successfully.")
    return agent_executor
