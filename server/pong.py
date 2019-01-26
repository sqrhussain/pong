import asyncio
import websockets
import json
import time
import numpy as np

# see: https://websockets.readthedocs.io/en/stable/index.html
# https://7webpages.com/blog/writing-online-multiplayer-game-with-python-asyncio-getting-asynchronous/


class Vec2d:
    def __init__(self, x=0., y=0.):
        self.x = float(x)
        self.y = float(y)

    def __add__(self, other):
        return Vec2d(self.x + other.x, self.y + other.y)

    def __mul__(self, other):
        return Vec2d(self.x * other, self.y * other)


width = 1080.
height = 720.
padding = {'w': 5, 'h': 5}
paddleSize = {'w': 20, 'h': 160}
ballRadius = 20

paddleStep = 20
ball = {
    'position': Vec2d(width / 2, height / 2),
    'velocity': Vec2d(0, 0)
}
velocity_increase = 0.05
paddles = [
    {'y': height / 2. + paddleSize['h'] / 2.},
    {'y': height / 2. + paddleSize['h'] / 2.}
]
ball_min_y = ballRadius
ball_max_y = height - ballRadius
ball_paddle_min_x = paddleSize['w'] + padding['w'] + ballRadius
ball_paddle_max_x = width - paddleSize['w'] - padding['w'] - ballRadius
paddle_min_y = 0
paddle_max_y = height - paddleSize['h']
FPS = 30
players_ws = []
player_names = []

score = [0,0]


def init_round():
	global ball
	sign = 1 - 2 * np.random.randint(2);
	vx = np.random.rand()*0.5 + 0.5;
	vy = np.sqrt(1-vx**2);
	ball = {
	    'position': Vec2d(width/2, height/2),
	    'velocity': Vec2d(sign * vx, vy-0.5).__mul__(400)
	}
	print('init: {}'.format(ball['position'].x))
def init_game():
    global score
    global paddles
    score = [0,0];
    paddles = [
        {'y': height / 2. - paddleSize['h'] / 2.},
        {'y': height / 2. - paddleSize['h'] / 2.}
    ]

async def onGameEnd(winner):
    print(winner)
    print(game_state_event('gameEnd',win=1))
    await (qs[winner]).put(game_state_event('gameEnd',win=1))
    await (qs[1-winner]).put(game_state_event('gameEnd',win=0))
    init_game();

queue = asyncio.Queue(10)
qs = [asyncio.Queue(10),asyncio.Queue(10)]

async def game_loop():
    # waitingForPlayers, playing or gameEnd
    game_state = 'waitingForPlayers'
    await queue.put(game_state_event(game_state))
    gameEndAt = 10

    init_game()
    rnd = 1;
    while True:
        print('game_state {}, ws set = {}'.format(game_state,len(players_ws)))
        await queue.put(game_state_event(game_state))
        if len(players_ws) < 2 and game_state == 'gameEnd':
        	game_state = 'waitingForPlayers'
        if len(players_ws) > 1 and game_state != 'playing':
            game_state = 'playing'
        if game_state == 'waitingForPlayers' or game_state == 'gameEnd':
            await asyncio.sleep(1)
            continue
        await queue.put(game_state_event(game_state))
        rnd = rnd +1;
        init_round()
        last_frame_time = time.time()
        while True:
            current_time = time.time()
            delta_time = current_time - last_frame_time
            last_frame_time = current_time

            new_position = ball['position'] + (ball['velocity'] * delta_time)

            if new_position.x > width or new_position.x < 0:
                add_score(int(new_position.x < 0)) # player 0 or player 1
                await queue.put(hit_event("goal"))
                await queue.put(score_event())
                if score[0] >= gameEndAt or score[1] >= gameEndAt:
                    await onGameEnd(score[1] > score[0])
                    game_state = 'gameEnd'
                sleep_time = 1. / FPS - (current_time - last_frame_time)
                if sleep_time > 0:
                    await asyncio.sleep(sleep_time)
                break


            # todo: send event to play sound
            if new_position.x > ball_paddle_max_x and new_position.x < width and \
                    new_position.y > paddles[1]['y'] - ballRadius and \
                    new_position.y < paddles[1]['y'] + paddleSize['h'] + ballRadius:
                await queue.put(hit_event("paddle"))
                new_position.x = ball_paddle_max_x
                ball['velocity'].x = -ball['velocity'].x
                ball['velocity'].x = ball['velocity'].x + (np.random.rand() - 0.5) * 20
                ball['velocity'].y = ball['velocity'].y + (np.random.rand() - 0.5) * 20
                ball['velocity'] += ball['velocity'] * velocity_increase
            elif new_position.x < ball_paddle_min_x and new_position.x > 0 and \
                    new_position.y > paddles[0]['y'] - ballRadius and \
                    new_position.y < paddles[0]['y'] + paddleSize['h'] + ballRadius:
                await queue.put(hit_event("paddle"))
                new_position.x = ball_paddle_min_x
                ball['velocity'].x = -ball['velocity'].x
                ball['velocity'].x = ball['velocity'].x + (np.random.rand() - 0.5) * 20
                ball['velocity'].y = ball['velocity'].y + (np.random.rand() - 0.5) * 20
                ball['velocity'] += ball['velocity'] * velocity_increase

            # todo: send event to play sound
            if new_position.y < ball_min_y:
                await queue.put(hit_event("wall"))
                # todo: make this more precise.
                new_position.y = ball_min_y
                ball['velocity'].y = -ball['velocity'].y
            elif new_position.y > ball_max_y:
                await queue.put(hit_event("wall"))
                # todo: make this more precise.
                new_position.y = ball_max_y
                ball['velocity'].y = -ball['velocity'].y

            ball['position'] = new_position

            sleep_time = 1. / FPS - (current_time - last_frame_time)
            if sleep_time > 0:
                await asyncio.sleep(sleep_time)

def score_event():
    return json.dumps({'type': 'score', 'score': score})

def ball_event():
    return json.dumps({'type': 'ball', 'position': ball['position'].__dict__, 'velocity': ball['velocity'].__dict__})

def paddle_event(player):
    return json.dumps({'type': 'paddle', 'player': player, **paddles[player]})

def game_state_event(state,win = -1):
	return json.dumps({'type': 'game_state', 'state': state, 'win' : win})

def hit_event(hitObject):
	return json.dumps({'type': 'hit', 'hitObject': hitObject})


def names_event():
	return json.dumps({'type': 'names', 'player1': player_names[0], 'player2': player_names[1]})


def add_score(player):
    score[player] = score[player] + 1;
    print(score)
    # await websocket.send(score_event())

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


async def consumer(websocket, message, player):
    msg_obj = json.loads(message)
    if msg_obj['type'] == 'move':
        move_paddle(player, msg_obj['direction'])
        await asyncio.wait([ws.send(paddle_event(0)) for ws in players_ws])
        await asyncio.wait([ws.send(paddle_event(1)) for ws in players_ws])
    elif msg_obj['type'] == 'playername':
        print(msg_obj['name'])
        player_names.append(msg_obj['name'])
        if len(player_names) > 1:
            await queue.put(names_event())


async def consumer_handler(websocket, path, player):
    while True:
        message = await websocket.recv()
        await consumer(websocket, message, player)


async def producer_handler(websocket, path):
    while True:
        await websocket.send(ball_event())
        await asyncio.sleep(0.1)


async def game_state_producer(websocket, path):
    while True:
        event = await queue.get()
        await asyncio.wait([ws.send(event) for ws in players_ws])
        print(event)

async def game_win_producer(websocket, path):
    while True:
        event = await (qs[0]).get()
        await players_ws[0].send(event)
        event = await (qs[1]).get()
        await players_ws[1].send(event)


# todo: on first connect send paddle positions
async def handler(websocket, path):
    players_ws.append(websocket)
    print('connect {}'.format(len(players_ws)))
    await queue.put(paddle_event(0))
    await queue.put(paddle_event(1))

    try:
        consumer_task = asyncio.ensure_future(
            consumer_handler(websocket, path, len(players_ws) - 1))
        producer_task1 = asyncio.ensure_future(
            producer_handler(websocket, path))
        producer_task2 = asyncio.ensure_future(
            game_state_producer(websocket,path))
        producer_task3 = asyncio.ensure_future(
            game_win_producer(websocket,path))
        done, pending = await asyncio.wait(
            [consumer_task, producer_task1, producer_task2,producer_task3],
            return_when=asyncio.FIRST_COMPLETED,
        )
        for task in pending:
            task.cancel()
    finally:
        print('unregister')
        players_ws.remove(websocket)


if __name__ == "__main__":
    start_server = websockets.serve(handler, 'localhost', 8765)
    all_tasks = asyncio.gather(game_loop(), start_server)

    asyncio.get_event_loop().run_until_complete(all_tasks)
    asyncio.get_event_loop().run_forever()
