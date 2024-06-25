from flask import Flask, render_template
import asyncio
import websockets
import threading

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

clients = []

async def handle_websocket(websocket, path):
    clients.append(websocket)
    try:
        async for message in websocket:
            for client in clients:
                if client != websocket:
                    await client.send(message)
    except websockets.ConnectionClosed:
        pass
    finally:
        clients.remove(websocket)

def start_websocket_server():
    asyncio.set_event_loop(asyncio.new_event_loop())
    server = websockets.serve(handle_websocket, "localhost", 6789)
    asyncio.get_event_loop().run_until_complete(server)
    asyncio.get_event_loop().run_forever()

if __name__ == '__main__':
    threading.Thread(target=start_websocket_server).start()
    app.run(debug=True)
