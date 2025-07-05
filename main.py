import asyncio
import json
import os
from aiohttp import web
from typing import Set, Dict, Any
from models import load_model_settings
from utils.message_helpers import make_reply, make_error

connected_clients: Set[web.WebSocketResponse] = set()

# Load environment variables from .env if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass

# Try loading required dependencies for LangChain-based workflow
try:
    from langchain_core.messages import HumanMessage
    from agents.supervisor import create_supervisor_workflow
    from utils.pretty_print import pretty_print_message, pretty_print_error
    from utils.message_helpers import make_message, make_error
    from utils.router import ROUTES
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    DEPENDENCIES_AVAILABLE = False

SUPERVISOR = create_supervisor_workflow()

async def create_space(user_request: str, ws: web.WebSocketResponse):
    if not DEPENDENCIES_AVAILABLE:
        raise ImportError("Dependencies not available.")

    initial_state = {
        "input": user_request,
        "messages": [HumanMessage(content=user_request)]
    }

    try:
        async for step in SUPERVISOR.astream(
            input=initial_state,
            stream_mode="values",
            config={"recursion_limit": 50}
        ):
            # ✅ Always check if it's a log
            if isinstance(step, dict):
                # ✅ Handle LOG type directly
                if step.get("type") == "LOG":
                    print(f"📤 Sending LOG to client: {step['content']}")
                    await ws.send_json(step)
                
                # ✅ Handle message from make_message() wrapper
                elif step.get("type") == "message" and "content" in step:
                    print(f"📤 Sending MESSAGE to client: {step['content']}")
                    await ws.send_json(step)
                
                # ✅ Handle full state with messages[] from LangGraph
                elif "messages" in step:
                    for msg in step["messages"]:
                        content = getattr(msg, "content", None)
                        if not content and isinstance(msg, dict):
                            content = msg.get("content")
                        if content and content.strip().lower() != user_request.strip().lower():
                            pretty_print_message(msg)
                            await ws.send_json(make_message(content))


    except Exception as e:
        pretty_print_error(f"Workflow error: {str(e)}")
        await ws.send_json(make_error(str(e)))

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
                        await ws.send_json(make_reply(["pong"]))
                    elif user_input == "session":
                        await ws.send_json(make_reply(["session acknowledged"]))
                    elif user_input.strip():
                        await create_space(user_input, ws)

                except Exception as e:
                    await ws.send_json(make_error(str(e)))

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
    load_model_settings()
    try:
        asyncio.run(start_combined_server())
    except KeyboardInterrupt:
        print("🛑 Server shutdown")
