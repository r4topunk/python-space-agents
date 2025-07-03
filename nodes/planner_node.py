import asyncio
from typing import AsyncGenerator, Dict, Any
from langchain_core.runnables import Runnable
from utils.message_helpers import make_log, make_message

async def planner_logic(state: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
    prompt = state.get("input", "")

    yield make_log("planner", "start", f"🧠 Planner starting: {prompt}")
    await asyncio.sleep(2.5)

    plan = {
        "grid": "12x10",
        "fidgets": ["rss", "image", "info", "social"]
    }

    yield make_message(f"Planned layout: {plan['grid']} with {len(plan['fidgets'])} fidgets")
    yield make_log("planner", "end", f"✅ Planner finished for: {prompt}")

    yield {
        **state,
        "messages": state.get("messages", []) + [{
            "type": "message",
            "content": f"Planned layout: {plan['grid']} with {len(plan['fidgets'])} fidgets"
        }],
        "plan": plan
    }

run_planner_node: Runnable = planner_logic
