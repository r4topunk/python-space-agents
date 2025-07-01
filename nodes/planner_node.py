# nodes/planner_node.py

import asyncio
from typing import AsyncGenerator, Dict, Any
from langchain_core.runnables import Runnable

async def planner_logic(state: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
    prompt = state.get("input", "")

    yield {
        "type": "LOG",
        "node": "planner",
        "status": "start",
        "content": f"🧠 Planner starting: {prompt}"
    }

    await asyncio.sleep(0.5)

    plan = {
        "grid": "12x10",
        "fidgets": ["rss", "image", "info", "social"]
    }

    new_message = {
        "type": "message",
        "content": f"Planned layout: {plan['grid']} with {len(plan['fidgets'])} fidgets"
    }

    yield {
        "type": "LOG",
        "node": "planner",
        "status": "end",
        "content": f"✅ Planner finished for: {prompt}"
    }

    yield {
        **state,
        "messages": state.get("messages", []) + [new_message],
        "plan": plan
    }

run_planner_node: Runnable = planner_logic
