import asyncio
import websockets
import json
from datetime import datetime

DEFAULT_MESSAGE = "create a space about nouns.wtf"

def timestamp():
    return datetime.now().strftime("%H:%M:%S")

HELP_TEXT = """
🔘 Commands:
  [P] Ping           → Check server
  [M] Message        → Send default message
  [C] Custom Message → Type your own message
  [H] Help           → Show this help again
  [Q] Quit           → Close connection
"""

async def handle_messages(ws):
    try:
        async for reply in ws:
            data = json.loads(reply)
            if not isinstance(data, dict):
                print(f"{timestamp()} 🟠 Unrecognized data: {data}")
                continue

            msg_type = data.get("type", "")
            # print(data)

            if msg_type == "LOG":
                node = data.get("node", "?").upper()
                status = data.get("status", "").upper()
                content = data.get("content", "")
                print(f"{timestamp()} 🛰️ [{node}] {status}: {content}")

            elif "LOG" in msg_type:
                node = data.get("name", "?").upper()
                status = data.get("status", "").upper()
                content = data.get("message", "")
                print(f"{timestamp()} 🛰️ [{node}] {status}: {content}")

            elif msg_type == "Reply" or msg_type == "REPLY":
                print(f"{timestamp()} 🟡 Final Reply:")
                for m in data.get("message", []):
                    if isinstance(m, dict):
                        print(f"💬 {m.get('type', 'Text')}: {m.get('content', '')}")
                    elif isinstance(m, str):
                        print(f"💬 {m}")

            elif msg_type == "message":
                print(f"{timestamp()} 💬 {data.get('content', '')}")

            elif msg_type.lower() == "session":
                session = data.get("session", {})
                print(f"{timestamp()} 🆔 Session: ID={session.get('client_id', 'unknown')} Status={session.get('status', 'unknown')}")

            elif "error" in data:
                print(f"{timestamp()} ❌ Error: {data.get('error')}")
            else:
                print(f"{timestamp()} 🟠 Unknown message type: {data}")
    except websockets.ConnectionClosed:
        print("🔴 Connection closed.")

async def send_commands(ws):
    print(HELP_TEXT)  # Show once on startup
    while True:
        key = await asyncio.to_thread(input, "🎮 Choose option: ")
        key = key.strip().lower()

        if key == "q":
            print("👋 Exiting.")
            await ws.send(json.dumps({"message": "session"}))
            await asyncio.sleep(0.2)
            await ws.close()
            break
        elif key == "p":
            await ws.send(json.dumps({"message": "ping"}))
        elif key == "m":
            await ws.send(json.dumps({"message": DEFAULT_MESSAGE}))
        elif key == "c":
            custom = await asyncio.to_thread(input, "📝 Enter your message: ")
            await ws.send(json.dumps({"message": custom}))
        elif key == "h":
            print(HELP_TEXT)
        else:
            print("❌ Unknown key. Type [H] for help.")

async def connect_with_retry(uri):
    while True:
        try:
            async with websockets.connect(uri) as ws:
                print(f"{timestamp()} 🟢 Connected to server.")
                await ws.send(json.dumps({"message": "session"}))
                await asyncio.gather(
                    handle_messages(ws),
                    send_commands(ws)
                )
        except (websockets.ConnectionClosedError, OSError) as e:
            print(f"{timestamp()} 🔁 Disconnected. Retrying in 3s... ({e})")
            await asyncio.sleep(3)
        except KeyboardInterrupt:
            print("👋 Exiting by user.")
            break

if __name__ == "__main__":
    asyncio.run(connect_with_retry("ws://localhost:10000"))
