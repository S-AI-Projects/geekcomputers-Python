# Pong Game in Codeskulptor

import random

try:
    import simplegui
except ImportError:
    simplegui = None

WIDTH = 600
HEIGHT = 400
BALL_RADIUS = 20
PAD_WIDTH = 8
PAD_HEIGHT = 80
HALF_PAD_WIDTH = PAD_WIDTH / 2
HALF_PAD_HEIGHT = PAD_HEIGHT / 2
LEFT = False
RIGHT = True
score1 = 0
score2 = 0
paddle1_pos = 0
paddle2_pos = 0
paddle1_vel = 0
paddle2_vel = 0


def compute_ball_velocity(direction, rand_fn=None):
    """Computes the initial velocity vector [vx, vy] based on launch direction.

    Preconditions & Invariants:
        - Direction RIGHT assigns positive horizontal velocity in range [120/60, 240/60] = [2.0, 4.0].
        - Direction LEFT assigns negative horizontal velocity in range [-240/60, -120/60] = [-4.0, -2.0].
        - Vertical velocity is always positive in range [60/60, 180/60] = [1.0, 3.0].

    Simplification:
        Extracts velocity vector derivation into a single coherent calculation,
        decoupling vector mathematics from global game-state mutations.
    """
    rf = rand_fn if rand_fn is not None else random.randrange
    horiz_speed = rf(120, 240) / 60
    vert_speed = rf(60, 180) / 60
    vx = horiz_speed if direction == RIGHT else -horiz_speed
    vy = vert_speed
    return [vx, vy]


def spawn_ball(direction):
    """Spawns ball at center table and assigns initial velocity according to direction."""
    global ball_pos, ball_vel  # these are vectors stored as lists
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    ball_vel = compute_ball_velocity(direction)


def reset():
    global ball_pos, score1, score2
    ball_pos = [WIDTH / 2, HEIGHT / 2]
    score1 = 0
    score2 = 0


def new_game():
    global paddle1_pos, paddle2_pos, paddle1_vel, paddle2_vel
    global score1, score2
    reset()
    spawn_ball(RIGHT)


def draw(canvas):
    global \
        paddle1_pos, \
        paddle2_pos, \
        ball_pos, \
        ball_vel, \
        paddle1_vel, \
        paddle2_vel, \
        BALL_RADIUS
    global score1, score2

    canvas.draw_line([WIDTH / 2, 0], [WIDTH / 2, HEIGHT], 1, "White")
    canvas.draw_line([PAD_WIDTH, 0], [PAD_WIDTH, HEIGHT], 1, "White")
    canvas.draw_line([WIDTH - PAD_WIDTH, 0], [WIDTH - PAD_WIDTH, HEIGHT], 1, "White")

    ball_pos[0] += ball_vel[0]
    ball_pos[1] += ball_vel[1]

    if (
        ball_pos[0] <= BALL_RADIUS + PAD_WIDTH
        or ball_pos[0] >= WIDTH - BALL_RADIUS - PAD_WIDTH
    ):
        ball_vel[0] = -ball_vel[0]
    elif (
        ball_pos[1] <= BALL_RADIUS + PAD_WIDTH
        or ball_pos[1] >= HEIGHT - BALL_RADIUS - PAD_WIDTH
    ):
        ball_vel[1] = -ball_vel[1]

    canvas.draw_circle(ball_pos, BALL_RADIUS, 1, "White", "White")

    paddle1_pos += paddle1_vel
    paddle2_pos += paddle2_vel

    if paddle1_pos <= -HEIGHT / 2 + PAD_HEIGHT / 2:
        paddle1_pos = -HEIGHT / 2 + PAD_HEIGHT / 2
    elif paddle1_pos >= HEIGHT / 2 - PAD_HEIGHT / 2:
        paddle1_pos = HEIGHT / 2 - PAD_HEIGHT / 2

    if paddle2_pos <= -HEIGHT / 2 + PAD_HEIGHT / 2:
        paddle2_pos = -HEIGHT / 2 + PAD_HEIGHT / 2
    elif paddle2_pos >= HEIGHT / 2 - PAD_HEIGHT / 2:
        paddle2_pos = HEIGHT / 2 - PAD_HEIGHT / 2

    canvas.draw_line(
        [PAD_WIDTH / 2, paddle1_pos + HEIGHT / 2 - PAD_HEIGHT / 2],
        [PAD_WIDTH / 2, paddle1_pos + PAD_HEIGHT / 2 + HEIGHT / 2],
        10,
        "White",
    )
    canvas.draw_line(
        [WIDTH - PAD_WIDTH / 2, paddle2_pos + HEIGHT / 2 - PAD_HEIGHT / 2],
        [WIDTH - PAD_WIDTH / 2, PAD_HEIGHT / 2 + paddle2_pos + HEIGHT / 2],
        10,
        "White",
    )

    if (
        ball_pos[1] <= (paddle1_pos + HEIGHT / 2 - PAD_HEIGHT / 2)
        or ball_pos[1] >= (paddle1_pos + PAD_HEIGHT / 2 + HEIGHT / 2)
    ) and ball_pos[0] == (PAD_WIDTH + BALL_RADIUS):
        score2 += 1
    else:
        pass

    if (
        ball_pos[1] <= (paddle2_pos + HEIGHT / 2 - PAD_HEIGHT / 2)
        or ball_pos[1] >= (paddle2_pos + PAD_HEIGHT / 2 + HEIGHT / 2)
    ) and ball_pos[0] == (WIDTH - PAD_WIDTH - BALL_RADIUS):
        score1 += 1
    else:
        pass

    canvas.draw_text(str(score1), (250, 30), 40, "White")
    canvas.draw_text(str(score2), (330, 30), 40, "White")


def keydown(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["down"]:
        paddle1_vel = 2
    elif key == simplegui.KEY_MAP["up"]:
        paddle1_vel = -2

    if key == simplegui.KEY_MAP["w"]:
        paddle2_vel = -2
    elif key == simplegui.KEY_MAP["s"]:
        paddle2_vel = 2


def keyup(key):
    global paddle1_vel, paddle2_vel
    if key == simplegui.KEY_MAP["down"] or key == simplegui.KEY_MAP["up"]:
        paddle1_vel = 0
    if key == simplegui.KEY_MAP["w"] or key == simplegui.KEY_MAP["s"]:
        paddle2_vel = 0


if simplegui is not None:
    frame = simplegui.create_frame("Pong", WIDTH, HEIGHT)
    frame.set_draw_handler(draw)
    frame.set_keydown_handler(keydown)
    frame.set_keyup_handler(keyup)
    frame.add_button("Restart", reset)

    new_game()
    print()
    frame.start()
