# nodes/builder_node.py

import asyncio
from typing import AsyncGenerator, Dict, Any
from langchain_core.runnables import Runnable

async def builder_logic(state: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
    prompt = state.get("input", "")
    yield {
        "type": "LOG",
        "node": "builder",
        "status": "start",
        "content": f"🔧 Builder starting for: {prompt}"
    }

    await asyncio.sleep(0.5)

    layout = {
        "grid": state.get("grid", "12x10"),
        "fidgets": state.get("designed_fidgets", [])
    }

    message = {
        "type": "message",
        "content": f"✅ Final layout generated with {len(layout['fidgets'])} fidgets"
    }

    yield {
        "type": "LOG",
        "node": "builder",
        "status": "end",
        "content": f"✅ Builder finished for: {prompt}"
    }

    yield {
        **state,
        "messages": state.get("messages", []) + [message],
        "output": layout
    }

run_builder_node: Runnable = builder_logic
