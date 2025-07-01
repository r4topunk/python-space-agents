import asyncio
import json
import os
from aiohttp import web
from typing import Set, Dict, Any

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

async def create_space(user_request: str, ws: web.WebSocketResponse):
    if not DEPENDENCIES_AVAILABLE:
        raise ImportError("Dependencies not available.")

    workflow = create_supervisor_workflow()
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
            if isinstance(step, dict) and step.get("type") == "LOG":
                await ws.send_json(step)
                continue

            if "messages" in step and isinstance(step["messages"], list):
                last = step["messages"][-1]
                pretty_print_message(last)

                content = getattr(last, "content", None) or last.get("content") if isinstance(last, dict) else None
                if content:
                    await ws.send_json({
                        "type": "message",
                        "content": content
                    })

    except Exception as e:
        pretty_print_error(f"Workflow error: {str(e)}")
        await ws.send_json({"status": "error", "error": str(e)})

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

                    await create_space(user_input, ws)

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
