import asyncio
from typing import AsyncGenerator, Dict, Any
from langchain_core.runnables import Runnable
from utils.message_helpers import make_log, make_message

async def designer_logic(state: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
    plan = state.get("plan", {})
    prompt = state.get("input", "")

    yield make_log("designer", "start", f"🎨 Designer starting for: {prompt}")
    await asyncio.sleep(2.5)

    fidgets = plan.get("fidgets", [])
    grid = plan.get("grid", "12x10")

    positions = [
        {
            "type": f,
            "x": (i % 4) * 3,
            "y": (i // 4) * 3,
            "w": 3,
            "h": 3
        }
        for i, f in enumerate(fidgets)
    ]

    yield make_message(f"Designed layout with {len(positions)} fidgets in grid {grid}")
    yield make_log("designer", "end", f"✅ Designer finished for: {prompt}")

    yield {
        **state,
        "messages": state.get("messages", []) + [{
            "type": "message",
            "content": f"Designed layout with {len(positions)} fidgets in grid {grid}"
        }],
        "designed_fidgets": positions,
        "grid": grid
    }

run_designer_node: Runnable = designer_logic
