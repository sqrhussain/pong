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
paddleStep = 20
ball = {
    'position': {
        'x': 5,
        'y': 5
    }
}
paddles = [
    {'y': 1},
    {'y': 1}
]


async def game_loop():
    while True:
        ball['position']['x'] += 5
        ball['position']['y'] += 5
        await asyncio.sleep(0.1)


def ball_event():
    return json.dumps({'type': 'ball', **ball})


def paddle_event(player):
    return json.dumps({'type': 'paddle', 'player': player, **paddles[player]})


async def consumer(websocket, message):
    msg_obj = json.loads(message)
    if msg_obj['type'] == 'move':
        if msg_obj['direction'] == 'up':
            paddles[0]['y'] -= paddleStep
        if msg_obj['direction'] == 'down':
            paddles[0]['y'] += paddleStep
        await websocket.send(paddle_event(0))
        await websocket.send(paddle_event(1))


async def consumer_handler(websocket, path):
    while True:
        message = await websocket.recv()
        await consumer(websocket, message)


async def producer_handler(websocket, path):
    while True:
        await websocket.send(ball_event())
        await asyncio.sleep(0.5)


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
