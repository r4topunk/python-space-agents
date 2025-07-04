import asyncio
from fastmcp import Client
from fastmcp.client.transports import StreamableHttpTransport
from langchain_core.runnables import RunnableLambda
from typing import AsyncGenerator, Dict, Any
from utils.message_helpers import make_log
from langgraph.config import get_stream_writer
import json

MCP_ENDPOINT = "http://localhost:8000/mcp"
transport = StreamableHttpTransport(url=MCP_ENDPOINT)

async def researcher_logic(state: Dict[str, Any]) -> AsyncGenerator[Dict[str, Any], None]:
    writer = get_stream_writer()
    prompt = state.get("input", "")

    writer({"type": "LOG", "node": "researcher", "status": "start", "content": f"Research started: {prompt}"})
    yield make_log("researcher", "start", f"🔍 Researcher starting: {prompt}")

    try:
        async with Client(transport) as client:
            await client.session.initialize()

            result = await client.call_tool("image_search", {
                "query": prompt,
                "max_results": 5,
                "min_quality_score": 80,
                "min_resolution": [1024, 768]
            })

            # ✅ Extract images from result.content
            text = result.content[0].text
            images = json.loads(text)

            yield make_log("researcher", "end", f"✅ Found {len(images)} images for '{prompt}'")

            yield {
                **state,
                "images": images,
                "messages": state.get("messages", []) + [{
                    "type": "message",
                    "content": f"📸 Found {len(images)} images for '{prompt}'"
                }]
            }

    except Exception as e:
        error_msg = f"❌ MCP request failed: {e}"
        yield make_log("researcher", "error", error_msg)
        yield {
            **state,
            "messages": state.get("messages", []) + [{
                "type": "message",
                "content": error_msg
            }]
        }

run_researcher_node = RunnableLambda(researcher_logic)
