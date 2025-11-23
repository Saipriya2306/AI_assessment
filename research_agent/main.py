# main.py
import os
import asyncio
import logfire
from dotenv import load_dotenv
import time

# Load environment variables BEFORE importing the agent
load_dotenv(override=True)

from agent import research_agent
logfire.configure()
logfire.instrument_pydantic_ai()

# Give logfire time to print its project URL message
time.sleep(1)

async def run_agent(user_message: str, history: list):
    """Runs the agent and logs the interaction."""
    logfire.info("User input received", message=user_message)

    result = await research_agent.run(user_message, message_history=history)

    logfire.info("Agent output generated", output=str(result.output))

    return result


async def main():
    print("Research Agent Ready! (type 'exit' / 'quit' / 'bye' to stop)")
    history = []

    while True:
        user_msg = await asyncio.to_thread(input, "You: ")

        if user_msg.lower() in ["exit", "quit", "bye"]:
            print("Goodbye!")
            break

        result = await run_agent(user_msg, history)

        print("Agent:", result.output)

        # Store messages for conversation continuity
        history = result.all_messages()


if __name__ == "__main__":
    asyncio.run(main())
