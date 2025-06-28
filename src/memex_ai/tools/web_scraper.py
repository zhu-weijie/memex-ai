# src/memex_ai/tools/web_scraper.py
import requests
from bs4 import BeautifulSoup
from langchain_core.tools import tool


@tool
def scrape_url(url: str) -> str:
    """Scrapes the visible text content from a given webpage URL.
    Use this tool when you need to answer a question about the content of a specific
    website."""
    print(f"🛠️ Scraping URL: {url}")
    try:
        response = requests.get(url, timeout=10)
        response.raise_for_status()

        soup = BeautifulSoup(response.text, "html.parser")

        for script_or_style in soup(["script", "style"]):
            script_or_style.decompose()

        return soup.get_text(separator="\n", strip=True)
    except requests.RequestException as e:
        return f"Error scraping URL: {e}"
