import asyncio
import json
import os
from aiohttp import web
from typing import List, Dict, Any, Set, cast

# Optional: load env vars
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Try to import dependencies
try:
    from langchain_core.messages import HumanMessage, AnyMessage
    from agents.supervisor import create_supervisor_workflow
    from utils.pretty_print import (
        pretty_print_message,
        pretty_print_step,
        pretty_print_error,
        pretty_print_success,
    )
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"❌ Import error: {e}")
    DEPENDENCIES_AVAILABLE = False

connected_clients: Set[web.WebSocketResponse] = set()

async def create_space(user_request: str) -> List[Dict[str, Any]]:
    if not DEPENDENCIES_AVAILABLE:
        raise ImportError("Missing dependencies.")
    
    try:
        workflow = create_supervisor_workflow()
        result = []

        async for step in workflow.astream(
            {"messages": cast(List[HumanMessage], [HumanMessage(content=user_request)])},
            stream_mode="values",
            config={"recursion_limit": 50}
        ):
            if "messages" in step and step["messages"]:
                last_message = step["messages"][-1]
                pretty_print_message(last_message)
                result.append(last_message)
        return result
    except Exception as error:
        pretty_print_error(f"Error: {str(error)}")
        raise error

async def websocket_handler(request):
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    connected_clients.add(ws)
    print("🟢 Client connected")

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                data = json.loads(msg.data)
                user_input = data.get("message", "")
                try:
                    results = await create_space(user_input)
                    await ws.send_json({
                        "status": "ok",
                        "steps": [msg.content for msg in results]
                    })
                except Exception as e:
                    await ws.send_json({"status": "error", "error": str(e)})
            elif msg.type == web.WSMsgType.ERROR:
                print(f"WebSocket error: {ws.exception()}")
    finally:
        connected_clients.remove(ws)
        print("🔴 Client disconnected")

    return ws

async def handle_status(request):
    return web.Response(text="✅ Agent is up and running!")

async def start_combined_server():
    app = web.Application()
 
    # Health check now at /status
    app.router.add_get("/status", handle_status)

    # WebSocket now at /
    app.router.add_get("/", websocket_handler)
    runner = web.AppRunner(app)
    await runner.setup()

    site = web.TCPSite(runner, "0.0.0.0", 10000)
    await site.start()

    print("🚀 Server (HTTP + WS) running on http://localhost:10000")
    await asyncio.Event().wait()

if __name__ == "__main__":
    try:
        asyncio.run(start_combined_server())
    except KeyboardInterrupt:
        print("🛑 Server shutdown")

# Simulated WebSocket message to create a space
async def send_create_space_message(user_request: str):
    message = {
        "message": user_request
    }
    # Simulate sending the message to the WebSocket handler
    # This is a placeholder for actual WebSocket communication
    print(f"Sending message to create space: {message}")
