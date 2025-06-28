# src/memex_ai/config.py
import os
from dotenv import load_dotenv


def get_project_root() -> str:
    """Returns the absolute path to the project root."""
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def load_api_key():
    """
    Loads the OpenAI API key from the .env file located in the project root.
    """
    project_root = get_project_root()
    dotenv_path = os.path.join(project_root, ".env")

    if not os.path.exists(dotenv_path):
        print(f"Warning: .env file not found at {dotenv_path}")
        return None

    load_dotenv(dotenv_path=dotenv_path)

    api_key = os.getenv("OPENAI_API_KEY")

    if not api_key:
        print("Warning: OPENAI_API_KEY is not set in the .env file.")

    return api_key


OPENAI_API_KEY = load_api_key()
