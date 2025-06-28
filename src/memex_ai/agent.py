# src/memex_ai/agent.py
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from .config import OPENAI_API_KEY

from .tools.web_scraper import scrape_url


def create_agent():
    """
    Creates and returns a new LangGraph agent equipped with tools.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set. Please check your .env file.")

    model = ChatOpenAI(model="gpt-4-turbo", temperature=0)

    system_prompt = """You are a helpful assistant. You have access to a special tool.

    Tool:
    - `scrape_url`: Use this tool to get the contents of a webpage. Pass the URL as the
    argument.

    Only use the tools when necessary. If the user asks you a question about a URL or a
    specific website's content, use the scrape_url tool.
    """

    tools = [scrape_url]

    agent_executor = create_react_agent(model, tools=tools, prompt=system_prompt)

    print("✅ AI Agent with web scraper created successfully.")
    return agent_executor
