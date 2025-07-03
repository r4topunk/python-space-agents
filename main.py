"""
Main execution script for the Python Space Agents system with performance optimizations.
"""
import asyncio
import json
import os
import sys
import time
from typing import Set, List, Dict, Any, cast
from aiohttp import web
from langchain_core.messages import HumanMessage, AnyMessage
import structlog

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.dev.ConsoleRenderer()
    ],
    wrapper_class=structlog.stdlib.BoundLogger,
    logger_factory=structlog.stdlib.LoggerFactory(),
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()

connected_clients: Set[web.WebSocketResponse] = set()

# Load environment variables from .env if available
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    logger.info("python-dotenv not available, using environment variables directly")
    # Try to load .env manually if it exists
    if os.path.exists('.env'):
        with open('.env', 'r') as f:
            for line in f:
                if '=' in line and not line.strip().startswith('#'):
                    key, value = line.strip().split('=', 1)
                    os.environ[key] = value

# Try loading required dependencies for LangChain-based workflow
try:
    from agents.supervisor import create_supervisor_workflow
    from utils.pretty_print import (
        pretty_print_message,
        pretty_print_step,
        pretty_print_error,
        pretty_print_success,
    )
    from utils.message_helpers import make_message, make_error, make_reply
    from utils.performance import performance_monitor, simple_cache
    from config.llm_config import clear_llm_cache
    DEPENDENCIES_AVAILABLE = True
    logger.info("All dependencies loaded successfully")
except ImportError as e:
    logger.error("Import error", error=str(e))
    print(f"❌ Import error: {e}")
    print("💡 Try running: ./venv/bin/pip install -r requirements.txt")
    print("💡 Or use: python run.py for demo mode")
    DEPENDENCIES_AVAILABLE = False

SUPERVISOR = create_supervisor_workflow()

@performance_monitor.time_operation("create_space")
async def create_space(user_request: str, ws: web.WebSocketResponse):
    """
    Create a space configuration based on user request with performance monitoring,
    streaming results back to the client.
    """
    if not DEPENDENCIES_AVAILABLE:
        raise ImportError("Dependencies not available.")

    start_time = time.time()
    logger.info("Starting space creation", request=user_request[:100])

    initial_state = {
        "input": user_request,
        "messages": [HumanMessage(content=user_request)]
    }

    try:
        step_count = 0
        async for step in SUPERVISOR.astream(
            input=initial_state,
            stream_mode="values",
            config={"recursion_limit": 50}
        ):
            step_count += 1
            if isinstance(step, dict):
                if step.get("type") == "LOG":
                    logger.info("Sending LOG to client", content=step.get('content'))
                    await ws.send_json(step)
                
                elif step.get("type") == "message" and "content" in step:
                    logger.info("Sending MESSAGE to client", content=step.get('content'))
                    await ws.send_json(step)
                
                elif "messages" in step:
                    for msg in step["messages"]:
                        content = getattr(msg, "content", None)
                        if not content and isinstance(msg, dict):
                            content = msg.get("content")
                        if content and content.strip().lower() != user_request.strip().lower():
                            pretty_print_message(msg)
                            await ws.send_json(make_message(content))

        duration = time.time() - start_time
        cache_stats = simple_cache.get_stats()
        performance_report = performance_monitor.get_report()
        
        logger.info(
            "Space creation completed",
            duration=round(duration, 2),
            steps=step_count,
            cache_hit_rate=cache_stats["hit_rate"],
            total_operations=performance_report["summary"]["total_operations"]
        )
        pretty_print_success(f"Space creation completed in {duration:.2f}s with {step_count} steps!")

    except Exception as e:
        duration = time.time() - start_time
        logger.error("Space creation failed", error=str(e), duration=round(duration, 2))
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
    try:
        asyncio.run(start_combined_server())
    except KeyboardInterrupt:
        print("🛑 Server shutdown")
