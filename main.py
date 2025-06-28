# main.py
import traceback
import typer
from memex_ai.agent import create_agent

app = typer.Typer()


@app.command()
def chat(
    thread_id: str = typer.Option(
        "default-session",
        "--thread-id",
        "-t",
        help="The conversation thread ID to use.",
    )
):
    """
    Starts a new chat session with the Memex AI assistant.
    """
    print("=" * 50)
    print("🚀 Memex AI is Online!")
    print(f"✅ Active Thread: {thread_id}")
    print("   (Use --thread-id <name> to switch sessions)")
    print("   (Type 'exit' to quit)")
    print("=" * 50)

    agent = create_agent()
    config = {"configurable": {"thread_id": thread_id}}

    while True:
        try:
            user_input = input("You: ").strip()

            if user_input.lower() == "exit":
                print("🤖 Assistant: Goodbye!")
                break

            if not user_input:
                continue

            response = agent.invoke(
                {"messages": [("human", user_input)]}, config=config
            )

            assistant_message = response["messages"][-1].content
            print(f"🤖 Assistant: {assistant_message}\n")

        except KeyboardInterrupt:
            print("\n🤖 Assistant: Goodbye!")
            break
        except Exception as e:
            print(f"An error occurred: {e}")
            traceback.print_exc()
            break


if __name__ == "__main__":
    app()
