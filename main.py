import asyncio
import json
import os
from aiohttp import web
from typing import Set, Dict, Any
from models import load_model_settings
from utils.message_helpers import make_reply, make_error
from langgraph.graph import StateGraph, END
from langchain_core.runnables import Runnable
from nodes.intent_extractor import intent_extractor
from nodes.planner_node import run_planner_node
from nodes.researcher_node import run_researcher_node
from nodes.designer_node import run_designer_node
from nodes.builder_node import run_builder_node

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
    from utils.pretty_print import pretty_print_message, pretty_print_error
    from utils.message_helpers import make_message
    DEPENDENCIES_AVAILABLE = True
except ImportError as e:
    print(f"❌ Missing dependency: {e}")
    DEPENDENCIES_AVAILABLE = False

async def create_supervisor_workflow() -> Runnable:
    workflow = StateGraph(Dict[str, Any])
    workflow.add_node("intent_extractor", intent_extractor)
    workflow.add_node("researcher", run_researcher_node)
    workflow.add_node("planner", run_planner_node)
    workflow.add_node("designer", run_designer_node)
    workflow.add_node("builder", run_builder_node)

    workflow.set_entry_point("intent_extractor")
    workflow.add_edge("intent_extractor", "researcher")
    workflow.add_conditional_edges("researcher", lambda state: "builder" if state.get("intent", {}).get("intent", "") == "image_search" else "planner", {
        "planner": "planner",
        "builder": "builder"
    })
    workflow.add_edge("planner", "designer")
    workflow.add_edge("designer", "builder")
    workflow.add_edge("builder", END)
    
    return workflow.compile()

async def create_space(user_request: str, ws: web.WebSocketResponse):
    if not DEPENDENCIES_AVAILABLE:
        await ws.send_json(make_error("Dependencies not available."))
        return

    initial_state = {
        "input": user_request,
        "messages": [HumanMessage(content=user_request)]
    }

    try:
        workflow = await create_supervisor_workflow()
        seen_messages = set()  # Track unique messages to avoid duplicates
        async for step in workflow.astream(
            input=initial_state,
            stream_mode="values",
            config={"recursion_limit": 50}
        ):
            if isinstance(step, dict):
                # Handle log messages
                if step.get("type") == "log":
                    print(f"📤 Sending LOG to client: {step.get('content')}")
                    await ws.send_json(step)

                # Handle builder_logs directly
                elif step.get("type") == "builder_logs":
                    print(f"📤 Sending BUILDER_LOGS to client: {json.dumps(step['message'], indent=2)}")
                    await ws.send_json(step)

                # Handle messages array
                elif "messages" in step:
                    for msg in step["messages"]:
                        if isinstance(msg, dict):
                            content = msg.get("content", "")
                            msg_key = f"{msg.get('type')}:{content}"
                            if msg_key in seen_messages:
                                continue  # Skip duplicates
                            seen_messages.add(msg_key)

                            if msg.get("type") == "builder_logs":
                                print(f"📤 Sending BUILDER_LOGS from messages: {json.dumps(msg['content'], indent=2)}")
                                await ws.send_json({"type": "builder_logs", "message": msg["content"]})
                            elif msg.get("type") == "message":
                                print(f"📤 Sending MESSAGE to client: {content}")
                                await ws.send_json(msg)
                        elif isinstance(msg, HumanMessage):
                            continue  # Skip user input echo
                        else:
                            content = getattr(msg, "content", "")
                            if content and content.strip().lower() != user_request.strip().lower():
                                msg_key = f"message:{content}"
                                if msg_key not in seen_messages:
                                    seen_messages.add(msg_key)
                                    print(f"📤 Sending MESSAGE to client: {content}")
                                    await ws.send_json(make_message(content))

                # Handle output (final_config)
                elif "output" in step:
                    print(f"📤 Sending BUILDER_LOGS from output: {json.dumps(step['output'], indent=2)}")
                    await ws.send_json({"type": "builder_logs", "message": step["output"]})

    except Exception as e:
        error_msg = f"Workflow error: {str(e)}"
        pretty_print_error(error_msg)
        await ws.send_json(make_error(error_msg))

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