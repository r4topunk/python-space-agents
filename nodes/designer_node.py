# nodes/designer_node.py

import asyncio
from typing import AsyncGenerator, Dict, Any
from langchain_core.runnables import Runnable

async def designer_logic(state: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
    plan = state.get("plan", {})
    prompt = state.get("input", "")

    yield {
        "type": "LOG",
        "node": "designer",
        "status": "start",
        "content": f"🎨 Designer starting for: {prompt}"
    }

    await asyncio.sleep(0.5)

    fidgets = plan.get("fidgets", [])
    grid = plan.get("grid", "12x10")

    # Assign positions just for illustration
    positions = []
    for i, f in enumerate(fidgets):
        positions.append({
            "type": f,
            "x": (i % 4) * 3,
            "y": (i // 4) * 3,
            "w": 3,
            "h": 3
        })

    message = {
        "type": "message",
        "content": f"Designed layout with {len(positions)} fidgets in grid {grid}"
    }

    yield {
        "type": "LOG",
        "node": "designer",
        "status": "end",
        "content": f"✅ Designer finished for: {prompt}"
    }

    yield {
        **state,
        "messages": state.get("messages", []) + [message],
        "designed_fidgets": positions,
        "grid": grid
    }

run_designer_node: Runnable = designer_logic
