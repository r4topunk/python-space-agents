import asyncio
import websockets
import json
from datetime import datetime

# === Config ===
SERVER_URL = "ws://localhost:10000"
# SERVER_URL = "wss://space-builder-server.onrender.com"
DEFAULT_MESSAGE = "bitcoin community"

# === UI Helpers ===
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
        x, y, w, h = item.get("x", 0), item.get("y", 0), item.get("w", 1), item.get("h", 1)

        if x + w > grid_width or y + h > grid_height:
            print(f"❌ Invalid position/size for: {i}")
            continue

        label = f"F{idx}"
        for dy in range(h):
            for dx in range(w):
                grid_y = y + dy
                grid_x = x + dx
                grid[grid_y][grid_x] = f"{label:>3}" if dy == 0 and dx == 0 else " ░ "
        # legend.append(f"{label} = {i}")
        legend.append(f"{label} = {i} → pos({x},{y}) size({w}x{h})")


    print("\n🧱 Grid Layout Preview:\n")
    for row in grid:
        print("".join(row))
    print("\n📘 Legend:")
    for l in legend:
        print("  ", l)
    print()

# === WebSocket Handlers ===
async def handle_messages(ws):
    builder_buffer = ""
    collecting_builder = False

    try:
        async for reply in ws:
            data = json.loads(reply)
            if not isinstance(data, dict):
                print(f"{timestamp()} 🟠 Unrecognized data: {data}")
                continue

            msg_type = data.get("type", "").lower()

            # --- Logs ---
            if msg_type == "log":
                print(f"{timestamp()} 🛰️ [{data.get('node', '?').upper()}] {data.get('status', '').upper()}: {data.get('content', '')}")

            elif "log" in msg_type and msg_type != "builder_logs":
                print(f"{timestamp()} 🛰️ [{data.get('name', '?').upper()}] {data.get('status', '').upper()}: {data.get('message', '')}")

            # --- Reply ---
            elif msg_type == "reply":
                print(f"{timestamp()} 🟡 Reply:")
                for m in data.get("message", []):
                    if isinstance(m, dict):
                        print(f"💬 {m.get('type', 'Text')}: {m.get('content', '')}")
                    elif isinstance(m, str):
                        print(f"💬 {m}")

            # --- Message ---
            elif msg_type == "message":
                print(f"{timestamp()} 💬 {data.get('content', '')}")

            # --- Session ---
            elif msg_type == "session":
                s = data.get("session", {})
                print(f"{timestamp()} 🆔 Session: ID={s.get('client_id', 'unknown')} Status={s.get('status', 'unknown')}")

            # --- Error ---
            elif "error" in data:
                print(f"{timestamp()} ❌ Error: {data.get('error')}")

            # --- Builder Logs (streamed JSON) ---
            elif msg_type == "builder_logs":
                for chunk in data.get("message", []):
                    if isinstance(chunk, str):
                        builder_buffer += chunk
                        collecting_builder = True

                try:
                    parsed = json.loads(builder_buffer)
                    print(f"\n{timestamp()} 🧩 Builder Output:\n")
                    print(json.dumps(parsed, indent=2))

                    layout = parsed.get("layoutDetails", {}).get("layoutConfig", {}).get("layout", [])
                    if layout:
                        render_terminal_grid(layout)

                    builder_buffer = ""
                    collecting_builder = False

                except json.JSONDecodeError:
                    continue  # Keep buffering
            else:
                print(f"{timestamp()} 🟠 Unknown message type: {data}")

    except websockets.ConnectionClosed:
        print("🔴 Connection closed.")

async def send_commands(ws):
    print(HELP_TEXT)
    print("Default Message: " + DEFAULT_MESSAGE)
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

# === Main ===
async def connect_with_retry(uri):
    while True:
        try:
            async with websockets.connect(uri) as ws:
                print(f"{timestamp()} 🟢 Connected to server.")
                await ws.send(json.dumps({"message": "session"}))
                await asyncio.gather(handle_messages(ws), send_commands(ws))
        except (websockets.ConnectionClosedError, OSError) as e:
            print(f"{timestamp()} 🔁 Disconnected. Retrying in 3s... ({e})")
            await asyncio.sleep(3)
        except KeyboardInterrupt:
            print("👋 Exiting by user.")
            break

if __name__ == "__main__":
    try:
        asyncio.get_running_loop().run_until_complete(connect_with_retry(SERVER_URL))
    except RuntimeError:
        asyncio.run(connect_with_retry(SERVER_URL))
