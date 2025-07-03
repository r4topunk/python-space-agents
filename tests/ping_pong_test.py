import asyncio
import json
import websockets

async def listen():
    uri = "ws://localhost:10000/"
    async with websockets.connect(uri) as websocket:
        await websocket.send_json({
                            "name": "TEST",
                            "type": "REPLY",
                            "message": "ping"
                        })
        print("Sent: ping")
        
        while True:
            message = await websocket.recv()
            print(f"Received message: {message}")
            data = json.loads(message)
            if data.get("message") == "pong":
                print("Received: pong")
                assert data.get("name") == "Ping Pong"
                assert data.get("type") == "Reply"
                print("Received: pong")

if __name__ == "__main__":
    asyncio.run(listen())