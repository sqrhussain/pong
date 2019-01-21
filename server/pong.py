import asyncio
import websockets
import datetime
import random
import json

import database_adapter #Database

# see: https://websockets.readthedocs.io/en/stable/index.html
# https://7webpages.com/blog/writing-online-multiplayer-game-with-python-asyncio-getting-asynchronous/


width = 1080
height = 720
paddleSize = {'w': 20, 'h': 160}
ballRadius = 20

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


def move_paddle(player, direction):
    if direction == 'up':
        new_y = paddles[player]['y'] - paddleStep
        if new_y < 0:
            new_y = 0
        paddles[player]['y'] = new_y
    if direction == 'down':
        new_y = paddles[player]['y'] + paddleStep
        max_paddle_y = height - paddleSize['h']
        if new_y > max_paddle_y:
            new_y = max_paddle_y
        paddles[player]['y'] = new_y


async def consumer(websocket, message):
    msg_obj = json.loads(message)
    if msg_obj['type'] == 'move':
        player = 0
        move_paddle(player, msg_obj['direction'])
        await websocket.send(paddle_event(player))


async def consumer_handler(websocket, path):
    while True:
        message = await websocket.recv()
        await consumer(websocket, message)


async def producer_handler(websocket, path):
    while True:
        await websocket.send(ball_event())
        await asyncio.sleep(0.5)

# todo: on first connect send paddle positions

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
