# agent.py
from pydantic_ai import Agent
from tools import get_research

# A simple Research Agent using pydantic-ai
model = "google-gla:gemini-2.5-flash"
research_agent = Agent(
    model,
    system_prompt=(
        "You are a research assistant. "
        "When users ask for information about a specific topic "
        "use the get_research tool with clear, specific keywords. "
        "For follow-up questions like 'elaborate' or 'more details', provide detailed explanations using your existing knowledge "
        "rather than calling the research tool again with vague terms. "
        "Always explain results clearly and simply."
    ),
    tools=[get_research],
)
