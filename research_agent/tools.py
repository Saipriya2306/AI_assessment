# tools.py
import os
import httpx
from typing import Any
from pydantic_ai import RunContext
import logfire

async def get_research(ctx: RunContext[Any], topic: str) -> str:
    """
    research tool.
    Tries DuckDuckGo first. If not available, returns simple local results.
    """

    with logfire.span("tool.get_research", topic=topic):
        logfire.info("Research tool started", topic=topic)

        try:
            async with httpx.AsyncClient(timeout=10.0) as client:
                res = await client.get(
                    "https://api.duckduckgo.com/",
                    params={"q": topic, "format": "json", "no_redirect": "1"},
                    headers={
                        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                        "Accept": "application/json, text/plain, */*",
                        "Accept-Language": "en-US,en;q=0.9",
                        "Accept-Encoding": "gzip, deflate",
                        "DNT": "1",
                        "Connection": "keep-alive",
                        "Upgrade-Insecure-Requests": "1"
                    },
                    timeout=30.0
                )
            data = res.json()

            # If the API returns useful info
            if data.get("AbstractText") and data["AbstractText"].strip():
                summary = data["AbstractText"]
                logfire.info("Live research completed", summary_length=len(summary))
                return f"Live research summary about '{topic}':\n{summary}"
            
            # Check for other possible data fields
            elif data.get("Answer") and data["Answer"].strip():
                summary = data["Answer"]
                logfire.info("Live research completed", summary_length=len(summary))
                return f"Live research summary about '{topic}':\n{summary}"
            
            # Try to get information from RelatedTopics
            elif data.get("RelatedTopics") and len(data["RelatedTopics"]) > 0:
                topics = []
                for item in data["RelatedTopics"][:3]:  # Get first 3 topics
                    if isinstance(item, dict) and item.get("Text"):
                        topics.append(f"• {item['Text']}")
                
                if topics:
                    summary = "\n".join(topics)
                    logfire.info("Live research completed from RelatedTopics", summary_length=len(summary))
                    return f"Live research about '{topic}':\n{summary}"

        except Exception as e:
            logfire.warn("Live research failed", error=str(e), error_type=type(e).__name__)

        # --- Offline fallback (always works) ---
        logfire.info("Using offline fallback research", topic=topic)
        return f"I couldn't find current information from external sources about '{topic}', but I can provide information from my knowledge base if you'd like me to explain this topic."
