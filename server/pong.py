import asyncio
import websockets
import datetime
import random
import json

# see: https://websockets.readthedocs.io/en/stable/index.html
# https://7webpages.com/blog/writing-online-multiplayer-game-with-python-asyncio-getting-asynchronous/


width = 300
height = 150
ball = {
    'position': {
        'x': 5,
        'y': 5
    }
}
paddle1 = {
    'y': 1
}
paddle2 = {
    'y': 1
}


async def game_loop():
    while True:
        ball['position']['y'] += 1
        await asyncio.sleep(1)


def ball_event():
    return json.dumps({'type': 'ball', **ball})


async def message_loop(websocket, path):
    while True:
        await websocket.send(ball_event())
        await asyncio.sleep(1)

start_server = websockets.serve(message_loop, 'localhost', 8765)
all_tasks = asyncio.gather(game_loop(), start_server)

asyncio.get_event_loop().run_until_complete(all_tasks)
asyncio.get_event_loop().run_forever()
