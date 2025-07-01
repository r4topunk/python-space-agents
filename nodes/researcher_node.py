import asyncio
from typing import AsyncGenerator, Dict, Any
from langchain_core.runnables import Runnable

# Simulated async node function
async def researcher_logic(state: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
    prompt = state.get("input", "")

    yield {
        "type": "LOG",
        "node": "researcher",
        "status": "start",
        "content": f"🔍 Researcher starting: {prompt}"
    }

    # Simulate the LLM / image / link / rss tool work
    # In real case, call your imageResearcher or multi-tool logic here
    await asyncio.sleep(1.5)  # simulate delay

    # You can modify this with real LLM logic and output
    new_message = {
        "type": "message",
        "content": f"Found resources for: {prompt}"
    }

    yield {
        "type": "LOG",
        "node": "researcher",
        "status": "end",
        "content": f"✅ Researcher finished for: {prompt}"
    }

    # Return updated state with the message
    yield {
        **state,
        "messages": state.get("messages", []) + [new_message]
    }

# Export runnable
run_researcher_node: Runnable = researcher_logic
