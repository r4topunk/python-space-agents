import asyncio
import websockets
import json

async def test():
    uri = "ws://localhost:10000"
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({"message": "build me a cool cyberpunk profile"}))
        reply = await ws.recv()
        data = json.loads(reply)

        print("🟡 Received:")
        messages = data.get("message", [])
        for m in messages:
            if isinstance(m, dict):
                print(f"💬 {m.get('type', 'Text')}: {m.get('content', '')}")
            elif isinstance(m, str):
                print(f"💬 {m}")
            else:
                print("❓ Unknown format:", m)

asyncio.run(test())
