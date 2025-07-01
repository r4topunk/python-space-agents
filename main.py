import asyncio
import json
import os
from aiohttp import web
from typing import List, Dict, Any, Set, cast

# Load environment variables if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Dependency check and imports
try:
    from langchain_core.messages import HumanMessage
    from agents.supervisor import create_supervisor_workflow
    from utils.pretty_print import (
        pretty_print_message,
        pretty_print_error,
    )
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    DEPENDENCIES_AVAILABLE = False

connected_clients: Set[web.WebSocketResponse] = set()

async def create_space(user_request: str) -> List[Dict[str, Any]]:
    if not DEPENDENCIES_AVAILABLE:
        raise ImportError("Dependencies not available.")

    workflow = create_supervisor_workflow()
    result = []

    initial_state = {
        "input": user_request,
        "messages": [HumanMessage(content=user_request)]
    }

    try:
        async for step in workflow.astream(
            initial_state,
            stream_mode="values",
            config={"recursion_limit": 50}
        ):
            if "messages" in step and step["messages"]:
                last = step["messages"][-1]
                pretty_print_message(last)
                result.append({"type": last.type, "content": last.content})
                await asyncio.sleep(1.1)  # 💤 Delay after each message (tune as needed)
        return result
    except Exception as e:
        pretty_print_error(f"Workflow error: {str(e)}")
        raise

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)
    connected_clients.add(ws)
    print("🟢 Client connected")

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                try:
                    data = json.loads(msg.data)
                    user_input = data.get("message", "")

                    if user_input == "ping":
                        await ws.send_json({
                            "name": "Ping Pong",
                            "type": "Reply",
                            "message": "pong"
                        })
                        continue

                    results = await create_space(user_input)
                    await ws.send_json({
                        "name": "Space Builder",
                        "type": "Reply",
                        # "message": [r.content for r in results]
                        "message": [r["content"] for r in results if "content" in r]
                    })

                except Exception as e:
                    await ws.send_json({"status": "error", "error": str(e)})

            elif msg.type == web.WSMsgType.ERROR:
                print(f"WebSocket error: {ws.exception()}")

    finally:
        connected_clients.remove(ws)
        print("🔴 Client disconnected")

    return ws

async def handle_status(_: web.Request):
    return web.Response(text="✅ Agent is running!")

async def start_combined_server():
    app = web.Application()
    app.router.add_get("/status", handle_status)
    app.router.add_get("/", websocket_handler)

    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()
    print("🚀 Server running on http://localhost:10000")

    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(start_combined_server())
    except KeyboardInterrupt:
        print("🛑 Server shutdown")
