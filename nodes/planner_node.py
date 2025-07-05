import asyncio
from typing import AsyncGenerator, Dict, Any
from langchain_core.runnables import RunnableLambda
from utils.message_helpers import make_log, make_message

async def planner_logic(state: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
    if not isinstance(state, dict):
        raise ValueError(f"Planner received unexpected state type: {type(state)} - {state}")

    prompt = state.get("input", "")
    intent = state.get("intent", {})
    images = state.get("images", [])

    yield make_log("planner", "start", f"📐 Planner analyzing layout for: {prompt}")

    # Extract intent signals
    subject = intent.get("subject", "unknown subject")
    mood = intent.get("mood", "default")
    purpose = intent.get("purpose", "inform")

    # Basic planning rules (will get smarter later)
    fidgets = []

    # Text block (intro)
    fidgets.append({
        "id": "text:intro",
        "type": "text",
        "title": f"What is {subject}?",
        "content": f"This space showcases curated content about {subject}.",
    })

    # Image gallery
    if images:
        fidgets.append({
            "id": "gallery:main",
            "type": "gallery",
            "images": images[:3]  # top 3
        })

    # Feed (placeholder for now)
    fidgets.append({
        "id": "feed:latest",
        "type": "feed",
        "platform": "X",
        "handle": f"{subject.replace(' ', '')}Official"
    })

    yield make_log("planner", "end", f"🧩 Planner selected {len(fidgets)} fidgets")

    yield {
        **state,
        "designed_fidgets": fidgets,
        "messages": state.get("messages", []) + [{
            "type": "message",
            "content": f"🧩 Planner prepared {len(fidgets)} fidgets for subject: {subject}"
        }]
    }

run_planner_node = RunnableLambda(planner_logic)
