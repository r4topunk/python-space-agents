import asyncio
import websockets
import json

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
        # Run input in a thread to avoid blocking event loop
        user_input = await asyncio.to_thread(input, "📤 Enter command (/ping, /message <text>, /exit): ")
        user_input = user_input.strip()

        if user_input == "/exit":
            print("👋 Exiting.")
            await ws.close()
            break
        elif user_input == "/ping":
            await ws.send(json.dumps({"message": "ping"}))
        elif user_input.startswith("/message "):
            content = user_input[len("/message "):]
            await ws.send(json.dumps({"message": content}))
        else:
            print("❌ Unknown command. Use /ping or /message <text>")

async def main():
    uri = "ws://localhost:10000"
    async with websockets.connect(uri) as ws:
        print("🟢 Connected to server.")
        await asyncio.gather(
            handle_messages(ws),
            send_commands(ws)
        )

asyncio.run(main())
