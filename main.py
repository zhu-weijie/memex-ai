# main.py
import traceback
from memex_ai.agent import create_agent


def run_cli():
    """
    Runs a command-line interface to chat with the agent.
    """
    print("=" * 50)
    print("🚀 Memex AI is Online! (Type 'exit' to quit)")
    print("=" * 50)

    agent = create_agent()

    config = {"configurable": {"thread_id": "user-cli-session-1"}}

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
    run_cli()
