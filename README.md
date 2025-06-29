# Memex AI

![Python 3.12](https://img.shields.io/badge/python-3.12-blue.svg)
![Poetry](https://img.shields.io/endpoint?url=https://python-poetry.org/badge/v0.json)
![LangGraph](https://img.shields.io/badge/LangGraph-0.5.0-blue)
![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)

A personalized AI assistant that remembers you. 🧠 Built with Python and LangGraph.

Memex AI is a command-line research assistant that overcomes the limitations of stateless chatbots. It uses a persistent SQLite backend to remember your conversation history across sessions and an in-memory store to recall key facts during a live session.

## ✨ Key Features

*   **Persistent Conversation History:** Never lose your train of thought. Memex AI saves your chat logs and can reference previous turns even after restarting the app.
*   **Interactive Session Management:** A user-friendly menu allows you to create new, named conversation threads or reload past ones.
*   **In-Session Factual Memory:** Tell the agent to remember key information (like a project code or a research topic), and it can recall it for the duration of that session.
*   **Dynamic Toolset:** The agent is equipped with tools to enhance its capabilities:
    *   **`scrape_url`**: Scrape text content from any webpage.
    *   **`list_tools`**: Ask the agent about its own capabilities.
*   **Rich CLI Experience:** A polished command-line interface with color and markdown rendering powered by the `rich` library.

## 🛠️ Technology Stack

*   **Core Logic:** Python 3.12
*   **AI Framework:** LangChain & LangGraph
*   **LLM:** OpenAI GPT-4-Turbo
*   **Dependency Management:** Poetry
*   **Database:** SQLite for persistent chat history
*   **CLI:** Rich

## 🚀 Getting Started

Follow these steps to get Memex AI running on your local machine.

### Prerequisites

*   **Git**
*   **Python 3.12**
*   **Poetry**

### 1. Clone the Repository

```bash
git clone https://github.com/zhu-weijie/memex-ai.git
cd memex-ai
```

### 2. Install Dependencies

Poetry will handle creating a virtual environment and installing all the necessary packages from the `poetry.lock` file.

```bash
poetry env use /opt/homebrew/bin/python3.12
poetry install
```

### 3. Configure Your API Key

Memex AI requires an OpenAI API key to function.

1.  Copy the example environment file:
    ```bash
    cp .env.example .env
    ```
2.  Open the newly created `.env` file in your editor and replace the placeholder with your actual OpenAI API key.
    ```
    OPENAI_API_KEY="sk-YourSecretApiKeyHere"
    ```
    **Note:** The `.env` file is included in `.gitignore` and will not be committed to the repository.

## 💻 How to Use

Run the application using Poetry. This will start the interactive session menu.

```bash
poetry run python main.py
```

From the menu, you can:
*   **Create a new session** by typing a new name (e.g., `research-on-mars`).
*   **Load a previous session** by typing its corresponding number.
*   Type `exit` to close the application.

Inside a chat session, type `exit` to return to the main menu.

### Example Session

```
$ poetry run python main.py

=== Memex AI Session Menu ===
No existing sessions found.

Options:
 - Enter a number to load a session.
 - Enter a new name to create a new session.
 - Type 'exit' to quit.
> project-dragonfly
==================================================
🚀 Memex AI is Online! | Session: project-dragonfly
   (Type 'exit' to quit this session)
==================================================
✅ Memex AI Agent created successfully.
You (project-dragonfly): Please remember that the primary goal is to analyze sci-fi book covers.

🤖 Assistant:
I've remembered that the primary goal is to analyze sci-fi book covers.

You (project-dragonfly): What are your capabilities?

🤖 Assistant:
Here are the tools I have available:
 - **scrape_url**: Scrapes the visible text content from a given webpage URL...
 - **manage_memory**: A tool for managing memories...
 - **search_memory**: A tool for searching memories...
 - **list_tools**: Lists the names and descriptions of all available tools...

You (project-dragonfly): exit
🤖 Assistant: Returning to main menu...

=== Memex AI Session Menu ===
Existing sessions:
  1: project-dragonfly

Options:
...
> 1
==================================================
🚀 Memex AI is Online! | Session: project-dragonfly
...
You (project-dragonfly): What was the primary goal I mentioned earlier?

🤖 Assistant:
The primary goal you mentioned is to analyze sci-fi book covers.
```

## 📄 License

This project is licensed under the MIT License.
