import asyncio
from typing import AsyncGenerator, Dict, Any
from langchain_core.runnables import Runnable
from utils.message_helpers import make_log, make_message
from langchain_core.runnables import RunnableLambda
from langgraph.config import get_stream_writer

async def researcher_logic(state: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
    writer = get_stream_writer()
    writer({"type": "LOG", "node": "researcher", "status": "start", "content": "Research started"})
    
    prompt = state.get("input", "")

    # Log start
    yield make_log("researcher", "start", f"🔍 Researcher starting: {prompt}")
    # Send a message (wrapped with our helper)
    yield make_message(f"🔍 Researcher starting...")

    print("🚨 Yielded researcher start log")
    await asyncio.sleep(1.5)  # simulate processing

    # Send a message (wrapped with our helper)
    yield make_message(f"Found resources for: {prompt}")

    # Log end
    yield make_log("researcher", "end", f"✅ Researcher finished for: {prompt}")

    # Update state with the message
    yield {
        **state,
        "messages": state.get("messages", []) + [{"type": "message", "content": f"Found resources for: {prompt}"}]
    }

# run_researcher_node: Runnable = researcher_logic
run_researcher_node: Runnable = RunnableLambda(researcher_logic)
