# main.py
import sqlite3
import traceback
from memex_ai.agent import create_agent


def get_existing_sessions(conn_string: str) -> list[str]:
    """Queries the checkpointer DB for all unique thread IDs."""
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
        print("\n=== Memex AI Session Menu ===")
        sessions = get_existing_sessions(db_file)

        if not sessions:
            print("No existing sessions found.")
        else:
            print("Existing sessions:")
            for i, session_id in enumerate(sessions):
                print(f"  {i + 1}: {session_id}")

        print("\nOptions:")
        print(" - Enter a number to load a session.")
        print(" - Enter a new name to create a new session.")
        print(" - Type 'exit' to quit.")

        choice = input("> ").strip()

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
    print("=" * 50)
    print(f"🚀 Memex AI is Online! | Session: {thread_id}")
    print("   (Type 'exit' to quit this session)")
    print("=" * 50)

    agent = create_agent()
    config = {"configurable": {"thread_id": thread_id}}

    while True:
        try:
            user_input = input(f"You ({thread_id}): ").strip()

            if user_input.lower() == "exit":
                print("🤖 Assistant: Returning to main menu...")
                break

            if not user_input:
                continue

            response = agent.invoke(
                {"messages": [("human", user_input)]}, config=config
            )

            assistant_message = response["messages"][-1].content
            print(f"🤖 Assistant: {assistant_message}\n")

        except KeyboardInterrupt:
            print("\n🤖 Assistant: Returning to main menu...")
            break
        except Exception:
            print("\nAn error occurred:\n")
            traceback.print_exc()
            break


if __name__ == "__main__":
    run_menu()
