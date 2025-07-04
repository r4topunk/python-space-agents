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

def render_terminal_grid(layout, grid_width=12, grid_height=10):
    grid = [[" . " for _ in range(grid_width)] for _ in range(grid_height)]
    legend = []

    for idx, item in enumerate(layout, 1):
        i = item.get("i", "?")
        x = item.get("x", 0)
        y = item.get("y", 0)
        w = item.get("w", 1)
        h = item.get("h", 1)

        # Validate bounds
        if x + w > grid_width or y + h > grid_height:
            print(f"❌ Invalid position/size for: {i}")
            continue

        label = f"F{idx}"
        for dy in range(h):
            for dx in range(w):
                if dy == 0 and dx == 0:
                    grid[y + dy][x + dx] = f"{label:>3}"
                else:
                    grid[y + dy][x + dx] = " ░ "

        legend.append(f"{label} = {i}")

    print("\n🧱 Grid Layout Preview:\n")
    for row in grid:
        print("".join(row))
    print("\n📘 Legend:")
    for l in legend:
        print("  ", l)
    print()

async def handle_messages(ws):
    try:
        async for reply in ws:
            data = json.loads(reply)
            if not isinstance(data, dict):
                print(f"{timestamp()} 🟠 Unrecognized data: {data}")
                continue

            msg_type = data.get("type", "")
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

            elif msg_type.lower() == "reply":
                print(f"{timestamp()} 🟡 Final Reply:")
                for m in data.get("message", []):
                    if isinstance(m, dict):
                        content = m.get("content", "")
                        print(f"💬 {m.get('type', 'Text')}: {content}")
                        if content.strip().startswith("{") and "layoutConfig" in content:
                            try:
                                parsed = json.loads(content)
                                layout = parsed.get("layoutDetails", {}).get("layoutConfig", {}).get("layout", [])
                                render_terminal_grid(layout)
                            except Exception as e:
                                print(f"⚠️ Could not render grid: {e}")
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
    print(HELP_TEXT)
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
    try:
        asyncio.get_running_loop().run_until_complete(
            connect_with_retry("wss://space-builder-server.onrender.com")
        )
    except RuntimeError:
        asyncio.run(connect_with_retry("wss://space-builder-server.onrender.com"))
