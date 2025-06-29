# main.py
import sqlite3
import traceback

from rich.console import Console
from rich.markdown import Markdown

from memex_ai.agent import create_agent

console = Console()


def get_existing_sessions(conn_string: str) -> list[str]:
    try:
        con = sqlite3.connect(conn_string)
        cursor = con.cursor()
        cursor.execute("SELECT DISTINCT thread_id FROM checkpoints")
        sessions = [row[0] for row in cursor.fetchall()]
        return sessions
    except sqlite3.Error:
        return []
    finally:
        if con:
            con.close()


def run_menu():
    """Displays the main menu to select or create a session."""
    db_file = "memory.sqlite"

    while True:
        console.print("\n[bold cyan]=== Memex AI Session Menu ===[/bold cyan]")
        sessions = get_existing_sessions(db_file)

        if not sessions:
            console.print("[yellow]No existing sessions found.[/yellow]")
        else:
            console.print("[bold]Existing sessions:[/bold]")
            for i, session_id in enumerate(sessions):
                console.print(f"  [green]{i + 1}[/green]: {session_id}")

        console.print("\n[bold]Options:[/bold]")
        console.print(" - Enter a number to load a session.")
        console.print(" - Enter a new name to create a new session.")
        console.print(" - Type 'exit' to quit.")

        choice = console.input("[bold]>[/bold] ").strip()

        if not choice:
            continue
        if choice.lower() == "exit":
            break

        thread_id = ""
        if choice.isdigit() and 1 <= int(choice) <= len(sessions):
            thread_id = sessions[int(choice) - 1]
        else:
            thread_id = choice

        chat_session(thread_id)


def chat_session(thread_id: str):
    """Starts a chat session with the given thread ID."""
    console.print("=" * 50)
    console.print(
        f"🚀 [bold green]Memex AI is Online! | Session: {thread_id}[/bold green]"
    )
    console.print("   (Type 'exit' to quit this session)")
    console.print("=" * 50)

    agent = create_agent()
    config = {"configurable": {"thread_id": thread_id}}

    while True:
        try:
            user_input = console.input(f"[bold]You ({thread_id}):[/bold] ").strip()

            if user_input.lower() == "exit":
                console.print(
                    "[yellow]🤖 Assistant: Returning to main menu...[/yellow]"
                )
                break

            if not user_input:
                continue

            response = agent.invoke(
                {"messages": [("human", user_input)]}, config=config
            )

            assistant_message = response["messages"][-1].content

            console.print("\n[bold]🤖 Assistant:[/bold]")
            console.print(Markdown(assistant_message))
            console.print("")

        except KeyboardInterrupt:
            console.print("\n[yellow]🤖 Assistant: Returning to main menu...[/yellow]")
            break
        except Exception:
            console.print("\n[bold red]An error occurred:[/bold red]\n")
            traceback.print_exc()
            break


if __name__ == "__main__":
    run_menu()
