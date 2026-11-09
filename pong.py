import pygame
import sys
import math
import random

# ================= CONFIG =================
WIDTH, HEIGHT = 800, 450
FPS = 60

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# ------- CONTROLS ----------
LEFT_UP = pygame.K_UP
LEFT_DOWN = pygame.K_DOWN
START_GAME = pygame.K_SPACE
RESET_GAME = pygame.K_r

# ---------- PADDLE & BALL ----------
PADDLE_WIDTH = 12
PADDLE_HEIGHT = 90
PADDLE_SPEED = 7
AI_PADDLE_SPEED = 6.5
AI_REACTION_ZONE = 50

BALL_SIZE = 14
BALL_START_SPEED = 5.0
BALL_SPEED_INCREMENT = 0.4
BALL_MAX_SPEED = 12.0
MAX_BOUNCE_ANGLE = math.radians(65) 
MIN_VERTICAL_SPEED = 1.2

# ==========================================

pygame.init()
pygame.mixer.init()

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Refined Pong")
clock = pygame.time.Clock()
font = pygame.font.SysFont(None, 48)

# ---------- PRE-GENERATE SOUNDS ----------
# Generating sounds once at startup prevents frame-stuttering
def create_beep(freq, duration):
    # Match the mixer's actual format so length and pitch come out as requested
    sample_rate, _, channels = pygame.mixer.get_init()
    n_samples = int(sample_rate * duration / 1000)
    buf = bytearray()
    for i in range(n_samples):
        t = i / sample_rate
        wave = int(32767 * 0.25 * math.sin(2 * math.pi * freq * t))
        buf += wave.to_bytes(2, "little", signed=True) * channels
    return pygame.mixer.Sound(buffer=bytes(buf))

SOUND_WALL = create_beep(300, 80)
SOUND_PADDLE = create_beep(600, 80)
SOUND_SCORE = create_beep(200, 150)

# ---------- OBJECTS ----------
left_paddle = pygame.Rect(30, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
right_paddle = pygame.Rect(WIDTH - 42, HEIGHT//2 - PADDLE_HEIGHT//2, PADDLE_WIDTH, PADDLE_HEIGHT)
ball = pygame.Rect(0, 0, BALL_SIZE, BALL_SIZE)

# Movement variables (using floats for precision)
ball_x, ball_y = float(WIDTH//2), float(HEIGHT//2)
ball_dx, ball_dy = 0.0, 0.0
right_paddle_y = float(right_paddle.y)  # Rect only stores whole pixels
left_score = 0
right_score = 0
game_started = False
last_paddle_hit = None

def reset_positions():
    global ball_dx, ball_dy, ball_x, ball_y, game_started, last_paddle_hit, right_paddle_y
    left_paddle.centery = HEIGHT // 2
    right_paddle.centery = HEIGHT // 2
    right_paddle_y = float(right_paddle.y)
    
    # ball_x / ball_y track the ball's top-left corner
    ball_x, ball_y = WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2
    ball.topleft = (ball_x, ball_y)

    # Initial launch angle
    angle = math.radians(20)
    ball_dx = random.choice((-1, 1)) * BALL_START_SPEED * math.cos(angle)
    ball_dy = random.choice((-1, 1)) * BALL_START_SPEED * math.sin(angle)

    game_started = False
    last_paddle_hit = None

def clamp_ball_angle(flatten=False):
    global ball_dx, ball_dy

    speed = math.hypot(ball_dx, ball_dy)

    # Compute angle using absolute horizontal component
    angle = math.atan2(ball_dy, abs(ball_dx))

    # Prevent too vertical
    if abs(angle) > MAX_BOUNCE_ANGLE:
        angle = math.copysign(MAX_BOUNCE_ANGLE, angle)

    # Slight flattening after wall bounce
    if flatten:
        angle *= 0.85

    # Rebuild velocity
    side = -1 if ball_dx < 0 else 1
    ball_dx = side * speed * math.cos(angle)
    ball_dy = speed * math.sin(angle)

    # 🔥 CRITICAL FIX: prevent too-horizontal motion
    if abs(ball_dy) < MIN_VERTICAL_SPEED:
        ball_dy = MIN_VERTICAL_SPEED * (1 if ball_dy >= 0 else -1)

        # Renormalize X to preserve speed
        ball_dx = side * math.sqrt(max(speed**2 - ball_dy**2, 0.1))


reset_positions()

# ---------- MAIN LOOP ----------
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.KEYDOWN:
            if event.key == START_GAME:
                game_started = True
            if event.key == RESET_GAME and not game_started:
                left_score = right_score = 0
                reset_positions()

    keys = pygame.key.get_pressed()
    moving_up = moving_down = False

    # Left Paddle (Player)
    if keys[LEFT_UP] and left_paddle.top > 10:
        left_paddle.top = max(10, left_paddle.top - PADDLE_SPEED)
        moving_up = True
    if keys[LEFT_DOWN] and left_paddle.bottom < HEIGHT - 10:
        left_paddle.bottom = min(HEIGHT - 10, left_paddle.bottom + PADDLE_SPEED)
        moving_down = True

    # Right Paddle (AI)
    if game_started and ball_dx > 0:
        if abs(right_paddle.centery - ball.centery) > AI_REACTION_ZONE:
            if right_paddle.centery < ball.centery:
                right_paddle_y += AI_PADDLE_SPEED
            else:
                right_paddle_y -= AI_PADDLE_SPEED
        
        # Keep AI in bounds
        right_paddle_y = max(10.0, min(HEIGHT - 10.0 - PADDLE_HEIGHT, right_paddle_y))
        right_paddle.y = round(right_paddle_y)

    # Ball Physics
    if game_started:
        ball_x += ball_dx
        ball_y += ball_dy
        ball.x, ball.y = int(ball_x), int(ball_y)

    # Wall Collision
    if ball.top <= 10:
        ball_y = 10
        ball_dy *= -1
        clamp_ball_angle(flatten=True)
        SOUND_WALL.play()
    elif ball.bottom >= HEIGHT - 10:
        ball_y = HEIGHT - 10 - BALL_SIZE
        ball_dy *= -1
        clamp_ball_angle(flatten=True)
        SOUND_WALL.play()

    # Paddle Collisions
    # Left Paddle
    if ball.colliderect(left_paddle) and ball_dx < 0:
        ball_x = left_paddle.right
        speed = min(math.hypot(ball_dx, ball_dy) + BALL_SPEED_INCREMENT, BALL_MAX_SPEED)
        
        angle = math.atan2(ball_dy, abs(ball_dx))
        if moving_up: angle -= math.radians(21)
        elif moving_down: angle += math.radians(21)
        
        angle = max(-MAX_BOUNCE_ANGLE, min(MAX_BOUNCE_ANGLE, angle))
        ball_dx = speed * math.cos(angle)
        ball_dy = speed * math.sin(angle)
        clamp_ball_angle()
        SOUND_PADDLE.play()
        last_paddle_hit = "left"

    # Right Paddle
    if ball.colliderect(right_paddle) and ball_dx > 0:
        ball_x = right_paddle.left - BALL_SIZE
        speed = min(math.hypot(ball_dx, ball_dy) + BALL_SPEED_INCREMENT, BALL_MAX_SPEED)
        
        angle = math.atan2(ball_dy, abs(ball_dx))
        ball_dx = -speed * math.cos(angle)
        ball_dy = speed * math.sin(angle)
        clamp_ball_angle()
        SOUND_PADDLE.play()
        last_paddle_hit = "right"

    # Scoring
    if ball.right < 0:
        right_score += 1
        SOUND_SCORE.play()
        reset_positions()
    elif ball.left > WIDTH:
        left_score += 1
        SOUND_SCORE.play()
        reset_positions()

    # ---------- DRAW ----------
    screen.fill(WHITE)
    pygame.draw.rect(screen, BLACK, (0, 0, WIDTH, HEIGHT), 10) # Border
    pygame.draw.line(screen, BLACK, (WIDTH//2, 10), (WIDTH//2, HEIGHT-10), 2) # Center line

    pygame.draw.rect(screen, BLACK, left_paddle)
    pygame.draw.rect(screen, BLACK, right_paddle)
    
    # Drawing ball with a small outline for style
    pygame.draw.ellipse(screen, WHITE, ball)
    pygame.draw.ellipse(screen, BLACK, ball, 2)

    # UI
    screen.blit(font.render(str(left_score), True, BLACK), (WIDTH//4, 20))
    screen.blit(font.render(str(right_score), True, BLACK), (WIDTH*3//4, 20))

    if not game_started:
        txt = font.render("PRESS SPACE TO START", True, BLACK)
        screen.blit(txt, (WIDTH//2 - txt.get_width()//2, HEIGHT - 60))

    pygame.display.flip()
    clock.tick(FPS)
