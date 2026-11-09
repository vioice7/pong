# Refined Pong (Pygame)

This project is a polished single-player Pong game written in Python using Pygame. The player controls the left paddle, while the right paddle is controlled by an AI opponent. The game focuses on smooth physics, controlled bounce angles, increasing difficulty, and simple synthesized sound effects.

---

## Requirements

* Python 3.8+
* Pygame

Install dependencies with:

```bash
pip install pygame
```

---

## How to Run

From the project directory:

```bash
python pong.py
```

---

## Controls

* Up Arrow: Move left paddle up
* Down Arrow: Move left paddle down
* Space: Start the round
* R: Reset scores (only when the game is not running)
* Close Window: Quit the game

---

## Gameplay Overview

* The game starts paused. Press Space to launch the ball.
* Each time the ball hits a paddle, its speed increases slightly up to a maximum limit.
* The angle of the ball depends on its current direction and paddle movement.
* The AI paddle reacts only when the ball is moving toward it and ignores small offsets (a dead zone) to keep gameplay fair.
* A point is scored when the opponent fails to return the ball.

---

## Game Mechanics Explained

### Ball Physics

* The ball uses floating-point positions for smooth movement.
* Bounce angles are clamped to prevent near-vertical or near-horizontal trajectories.
* After wall collisions, the angle is slightly flattened to keep rallies interesting.
* A minimum vertical speed is enforced to avoid endless horizontal motion.

### Paddle Collisions

* Paddle hits increase ball speed gradually.
* Player paddle movement (up or down) slightly modifies the bounce angle, allowing controlled shots.
* Maximum bounce angle is limited to maintain predictable gameplay.

### AI Behavior

* The AI paddle only reacts when the ball is traveling toward it.
* A reaction zone prevents perfect tracking, making the AI beatable.
* The AI paddle moves slightly slower than the player's paddle.

---

## Sound System

All sounds are generated programmatically at startup:

* Wall hit: Low-frequency beep
* Paddle hit: Higher-frequency beep
* Score: Longer, lower-frequency beep

Pre-generating sounds avoids runtime stuttering.

---

## Screen Layout

* White background with a black border
* Center dividing line
* Left and right scores displayed at the top
* Start prompt shown when the game is paused

---

## Configuration

Key values can be adjusted at the top of the script:

* Window size and FPS
* Paddle size and speed
* Ball speed, acceleration, and angle limits
* AI difficulty parameters

This makes it easy to tweak difficulty or gameplay feel.

---

## Notes

* The game loop runs at a fixed frame rate for consistent physics.
* Resetting the game recenters paddles and relaunches the ball with a controlled starting angle.
* The project is designed as a clean, extensible base for adding menus, multiplayer, or visual effects.
