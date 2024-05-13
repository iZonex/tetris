
# Tetris Clone in Curses

<img width="577" alt="Screenshot 2024-05-13 at 20 11 45" src="https://github.com/iZonex/tetris/assets/2759749/5817550d-a709-4f79-aab5-3912fee84f56">

This is a simple clone of the classic Tetris game implemented in Python using the `curses` library. It runs in the terminal and features classic Tetris gameplay with increasing difficulty as the game progresses.

## Game Description

In this Tetris clone, players must manipulate a random sequence of Tetriminoes, which fall into the playing area. The aim is to create a horizontal line of ten blocks without gaps. When such a line is created, it disappears, and any block above the deleted line will fall. As the game progresses, Tetriminoes fall faster, and the game ends when the stack of Tetriminoes reaches the top of the playing area.

## Features

- Colorful terminal graphics using `curses`.
- Increasing speed as the game progresses.
- Score tracking and display of the next piece.
- Simple keyboard controls: UP to rotate, LEFT and RIGHT to move, DOWN to speed up the fall.

## Prerequisites

To run this game, you will need:

- Python 3.x installed on your system.
- A Unix-like terminal (Linux, macOS terminal, or Windows Subsystem for Linux).

## Installation

1. Clone this repository to your local machine:
   ```bash
   git clone https://github.com/your-username/tetris-curses.git
   cd tetris-curses
   ```

2. No additional libraries are required as the script uses the built-in `curses` module which is available in the Python standard library for Unix-like systems.

## Running the Game

To start the game, simply run the Python script:

```bash
python3 tetris.py
```

Make sure you are in the directory containing `tetris.py`.

## Controls

- **Arrow Up**: Rotate the Tetrimino.
- **Arrow Left**: Move the Tetrimino left.
- **Arrow Right**: Move the Tetrimino right.
- **Arrow Down**: Speed up the Tetrimino's fall.
- **R**: Restart the game.
- **Q**: Quit the game.

Enjoy playing the game and try to beat your high score!
