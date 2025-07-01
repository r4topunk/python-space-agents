import asyncio
import websockets

async def listen():
    uri = "ws://localhost:10000/ws"
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
            if message == "pong":
                print("Received: pong")

if __name__ == "__main__":
    asyncio.run(listen())