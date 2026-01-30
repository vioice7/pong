````
# PONG GAMING

A minimalist, high-performance **Pong clone** built with **Python** and **Pygame**.  
This version features dynamic ball physics, increasing difficulty, and a refined black-and-white aesthetic.

---

## Features

- **Dynamic Physics**  
  Ball trajectory changes based on where it strikes the paddle.  
  Hitting the edges creates sharper angles.

- **Difficulty Scaling**  
  The ball speed increases by **5%** with every successful return, ensuring fast-paced gameplay.

- **Arcade UI**  
  Includes a *“Press Space”* start sequence and a professional scoring display with dashed center lines.

- **Clean Code**  
  Fully commented and organized for easy modification or educational use.

---

## Prerequisites

You must have **Python 3.x** and the **Pygame** library installed.

```bash
pip install pygame
````

---

## Controls

| Action             | Left Player (P1) | Right Player (P2) |
| ------------------ | ---------------- | ----------------- |
| Move Up            | Q                | P                 |
| Move Down          | A                | L                 |
| Start / Serve Ball | SPACE            | SPACE             |
| Reset Game / Score | R                | R                 |

---

## Installation & Execution

1. Clone the repository or download the source code.
2. Open your terminal or command prompt.
3. Navigate to the project directory.
4. Run the game:

```bash
python pong.py
```

---

## Gameplay Mechanics

* **Scoring**
  The first player to miss the ball gives a point to the opponent.

* **The Serve**
  The ball resets to the center and serves toward the player who just conceded a point.

* **Physics Engine**
  The ball’s vertical velocity is calculated as:

```text
Velocity = (Hit Position / Half Paddle Height) * Base Speed
```

---

## License

This project is open-source and available under the **MIT License** © 2026 .
