# test_ws.py
import asyncio
import websockets
import json

async def test():
    uri = "ws://localhost:10000"
    async with websockets.connect(uri) as ws:
        await ws.send(json.dumps({
            "type": "UserMessage",
            "name": "Tester",
            "message": "build me a cool cyberpunk profile"
        }))
        while True:
            reply = await ws.recv()
            print("🟡 Received:", reply)

asyncio.run(test())
