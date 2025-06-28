# src/memex_ai/agent.py
from langchain_openai import ChatOpenAI
from langgraph.prebuilt import create_react_agent

from .config import OPENAI_API_KEY


def create_agent():
    """
    Creates and returns a new LangGraph agent.
    """
    if not OPENAI_API_KEY:
        raise ValueError("OPENAI_API_KEY is not set. Please check your .env file.")

    model = ChatOpenAI(model="gpt-4-turbo", temperature=0)

    system_prompt = "You are a helpful assistant."

    agent_executor = create_react_agent(model, tools=[], prompt=system_prompt)

    print("✅ AI Agent created successfully.")  # ✅ means success
    return agent_executor
