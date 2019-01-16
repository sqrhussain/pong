import asyncio
import websockets
import datetime
import random
import json

import database_adapter #Database

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


def paddle_event(player):
    #return json.dumps({'type': 'paddle', 'player': player, 'y': y})
    return json.dumps({'type': 'paddle', 'player': player, **paddle1});


async def consumer(message):
    msg_obj = json.loads(message)
    if msg_obj['type'] == 'move':
        print('move msg!')
        if msg_obj['direction'] == 'up':
            paddle1['y'] -= 1
        if msg_obj['direction'] == 'down':
            paddle1['y'] += 1


async def producer():
    await asyncio.sleep(1)
    return paddle_event(1)


async def consumer_handler(websocket, path):
    while True:
        message = await websocket.recv()
        await consumer(message)


async def producer_handler(websocket, path):
    while True:
        message = await producer()
        await websocket.send(message)


async def handler(websocket, path):
    consumer_task = asyncio.ensure_future(
        consumer_handler(websocket, path))
    producer_task = asyncio.ensure_future(
        producer_handler(websocket, path))
    done, pending = await asyncio.wait(
        [consumer_task, producer_task],
        return_when=asyncio.FIRST_COMPLETED,
    )
    for task in pending:
        task.cancel()
 

start_server = websockets.serve(handler, 'localhost', 8765)
all_tasks = asyncio.gather(game_loop(), start_server)

asyncio.get_event_loop().run_until_complete(all_tasks)
asyncio.get_event_loop().run_forever()
