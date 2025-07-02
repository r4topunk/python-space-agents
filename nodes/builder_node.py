import asyncio
from typing import AsyncGenerator, Dict, Any
from langchain_core.runnables import Runnable
from utils.message_helpers import make_log, make_message

async def builder_logic(state: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
    prompt = state.get("input", "")
    yield make_log("builder", "start", f"🔧 Builder starting for: {prompt}")

    await asyncio.sleep(0.5)

    layout = {
        "grid": state.get("grid", "12x10"),
        "fidgets": state.get("designed_fidgets", [])
    }

    message_content = f"✅ Final layout generated with {len(layout['fidgets'])} fidgets"
    yield make_message(message_content)
    yield make_log("builder", "end", f"✅ Builder finished for: {prompt}")

    yield {
        **state,
        "messages": state.get("messages", []) + [{
            "type": "message",
            "content": message_content
        }],
        "output": layout
    }

run_builder_node: Runnable = builder_logic
