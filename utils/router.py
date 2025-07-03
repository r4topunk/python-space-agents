# utils/router.py
import uuid
from aiohttp import web
from utils.message_helpers import make_reply, make_log

# Store client IDs by WebSocket instance
client_ids = {}

def get_client_id(ws: web.WebSocketResponse) -> str:
    if ws not in client_ids:
        client_ids[ws] = str(uuid.uuid4())
    return client_ids[ws]

async def handle_ping(ws: web.WebSocketResponse):
    await ws.send_json(make_reply(["pong"]))
    await ws.send_json(make_log("server", "info", "✅ Pong sent"))

async def handle_id(ws: web.WebSocketResponse):
    cid = get_client_id(ws)
    await ws.send_json(make_reply([f"🆔 Client ID: {cid}"]))

async def handle_session(ws: web.WebSocketResponse):
    cid = get_client_id(ws)
    session_data = {
        "client_id": cid,
        "status": "active",
        "connected": True,
    }
    await ws.send_json({
        "type": "Session",
        "session": session_data
    })

async def handle_status(ws: web.WebSocketResponse):
    await ws.send_json(make_reply(["✅ Server is running"]))
    await ws.send_json(make_log("server", "info", "🟢 Status checked"))

ROUTES = {
    "ping": handle_ping,
    "id": handle_id,
    "session": handle_session,
    "status": handle_status,
}
