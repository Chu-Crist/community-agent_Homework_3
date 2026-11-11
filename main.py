
from agent import ask_agent


def main():

    print("=" * 55)
    print("       COMMUNITY ANALYSIS AI AGENT")
    print("=" * 55)

    print("Welcome! Ask me questions about community networks.")
    print("Type 'exit' or 'quit' to stop.\n")

    while True:

        user_question = input("You: ").strip()

        if user_question.lower() in ["exit", "quit"]:
            print("Agent: Goodbye!")
            break

        if not user_question:
            print("Agent: Please enter a question.\n")
            continue

        try:
            print("\nAgent: Thinking...\n")

            answer = ask_agent(user_question)

            print("Agent:", answer)
            print()

        except Exception as error:
            print(f"Agent: Something went wrong: {error}\n")


if __name__ == "__main__":
    main()
