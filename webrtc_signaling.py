import websockets
import binascii
import asyncio
import os

clients = {}
async def signal(websocket, path):
    client_id = binascii.hexlify(os.urandom(8))
    clients[client_id] = websocket
    try:
        async for message in websocket:
            print(message)
            for c in clients.values():
                if c != websocket:
                    await c.send(message)
    finally:
        clients.pop(client_id)
    
asyncio.get_event_loop().run_until_complete(websockets.serve(signal, "0.0.0.0", 8188))
asyncio.get_event_loop().run_forever()
