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
padding = {'w': 5, 'h': 5}
paddleSize = {'w': 20, 'h': 160}
ballRadius = 20

paddleStep = 20
ball = {
    'position': Vec2d(5, 5),
    'velocity': Vec2d(5, 10)
}
paddles = [
    {'y': 1},
    {'y': 1}
]
ball_min_y = ballRadius
ball_max_y = height - ballRadius
ball_paddle_min_x = paddleSize['w'] + padding['w'] + ballRadius
ball_paddle_max_x = width - paddleSize['w'] - padding['w'] - ballRadius
paddle_min_y = 0
paddle_max_y = height - paddleSize['h']


async def game_loop():
    while True:
        new_position = ball['position'] + ball['velocity']
        # todo: send event to play sound
        if new_position.y < ball_min_y:
            # todo: make this more precise.
            new_position.y = ball_min_y
            ball['velocity'].y = -ball['velocity'].y
        elif new_position.y > ball_max_y:
            # todo: make this more precise.
            new_position.y = ball_max_y
            ball['velocity'].y = -ball['velocity'].y
        # todo: check if paddle is there or not
        if new_position.x > ball_paddle_max_x:
            new_position.x = ball_paddle_max_x
            ball['velocity'].x = -ball['velocity'].x
        elif new_position.x < ball_paddle_min_x:
            new_position.x = ball_paddle_min_x
            ball['velocity'].x = -ball['velocity'].x
        ball['position'] = new_position
        await asyncio.sleep(0.1)


def ball_event():
    return json.dumps({'type': 'ball', 'position': ball['position'].__dict__, 'velocity': ball['velocity'].__dict__})


def paddle_event(player):
    return json.dumps({'type': 'paddle', 'player': player, **paddles[player]})


def move_paddle(player, direction):
    if direction == 'up':
        new_y = paddles[player]['y'] - paddleStep
        if new_y < paddle_min_y:
            new_y = paddle_min_y
        paddles[player]['y'] = new_y
    if direction == 'down':
        new_y = paddles[player]['y'] + paddleStep
        if new_y > paddle_max_y:
            new_y = paddle_max_y
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
