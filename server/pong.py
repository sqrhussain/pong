import asyncio
import websockets
import json

# see: https://websockets.readthedocs.io/en/stable/index.html
# https://7webpages.com/blog/writing-online-multiplayer-game-with-python-asyncio-getting-asynchronous/


# todo: move to module
class Vec2d:
    def __init__(self, x=0, y=0):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)


width = 1080
height = 720
paddleSize = {'w': 20, 'h': 160}
ballRadius = 20

paddleStep = 20
ball = {
    'position': Vec2d(5, 5),
    'velocity': Vec2d(1, 5)
}
paddles = [
    {'y': 1},
    {'y': 1}
]


async def game_loop():
    while True:
        new_position = ball['position'] + ball['velocity']
        min_y = (ballRadius / 2)
        max_y = height - (ballRadius / 2)
        if new_position.y < min_y:
            # todo: make this more precise.
            new_position.y = min_y
            ball['velocity'].y = -ball['velocity'].y
        elif new_position.y > max_y:
            # todo: make this more precise.
            new_position.y = max_y
            ball['velocity'].y = -ball['velocity'].y
        ball['position'] = new_position
        await asyncio.sleep(0.1)


def ball_event():
    return json.dumps({'type': 'ball', 'position': ball['position'].__dict__, 'velocity': ball['velocity'].__dict__})


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


if __name__ == "__main__":
    start_server = websockets.serve(handler, 'localhost', 8765)
    all_tasks = asyncio.gather(game_loop(), start_server)

    asyncio.get_event_loop().run_until_complete(all_tasks)
    asyncio.get_event_loop().run_forever()
