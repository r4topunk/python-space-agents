import asyncio
import websockets
import json

DEFAULT_MESSAGE = "this is a test"

async def handle_messages(ws):
    try:
        async for reply in ws:
            data = json.loads(reply)
            print("🟡 Received:")
            if isinstance(data, dict):
                msg_type = data.get("type", "")
                if msg_type == "Reply":
                    messages = data.get("message", [])
                    for m in messages:
                        if isinstance(m, dict):
                            print(f"💬 {m.get('type', 'Text')}: {m.get('content', '')}")
                        elif isinstance(m, str):
                            print(f"💬 {m}")
                elif msg_type == "LOG":
                    print(f"📝 LOG: {data.get('content', '')}")
                elif "error" in data:
                    print(f"❌ Error: {data.get('error')}")
                else:
                    print(data)
            else:
                print(data)
    except websockets.ConnectionClosed:
        print("🔴 Connection closed.")

async def send_commands(ws):
    while True:
        print("\n🔘 Commands: [P]ing | [M]essage | [C]ustom | [Q]uit")
        key = await asyncio.to_thread(input, "🎮 Choose option: ")
        key = key.strip().lower()

        if key == "q":
            print("👋 Exiting.")
            await ws.close()
            break
        elif key == "p":
            await ws.send(json.dumps({"message": "ping"}))
        elif key == "m":
            await ws.send(json.dumps({"message": DEFAULT_MESSAGE}))
        elif key == "c":
            custom = await asyncio.to_thread(input, "📝 Enter your message: ")
            await ws.send(json.dumps({"message": custom}))
        else:
            print("❌ Unknown key. Use P, M, C, or Q.")

async def connect_with_retry(uri):
    while True:
        try:
            async with websockets.connect(uri) as ws:
                print("🟢 Connected to server.")
                await asyncio.gather(
                    handle_messages(ws),
                    send_commands(ws)
                )
        except (websockets.ConnectionClosedError, OSError) as e:
            print(f"🔁 Disconnected. Retrying in 3s... ({e})")
            await asyncio.sleep(3)
        except KeyboardInterrupt:
            print("👋 Exiting by user.")
            break

asyncio.run(connect_with_retry("ws://localhost:10000"))
