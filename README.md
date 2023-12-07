# Novation mini arcade

This repository is a collection of simple arcade games for the Novation Launchpad Mini. The games are written in Python and use novation-launchpad to interface with the Launchpad Mini. It should work with any launchpad with a 8x8 grid of buttons.

## Demo
| Tetris | Pong | Space Invaders | Flappy Bird |
| --- | --- | --- | --- |
| ![Tetris](videos/tetris.gif) | ![Pong](videos/pong.gif) | ![Space Invaders](videos/space_invaders.gif) | ![Flappy Bird](videos/flappy.gif) |

## Installation
All dependencies are listed in `requirements.txt`. To install them, run `pip install -r requirements.txt`.

## Usage
To run a game, run `python <game>.py`. For example, to run pong, run `python pong.py`.

Controls are usually the bottom row of buttons (moving left and right), the "H" button (in Tetris - for going down faster) and any other button (shooting, rotating).

## Development
I'm not planning on having an active development. It was just a fun little project I did in a few days. You are always welcome to make a pull request with more games or improvements.

The code is not optimised at all. There's many places where it could be improved. As an overview, all games are implemented as a class that inherits from `LaunchGame` in `launchgame.py`. The `LaunchGame` class handles the communication with the Launchpad Mini and the main loop. The function running the game is called `run`, and each iteration it calls a `step` function which should be implemented by the game. The game should ideally not touch any graphics or buttons directly, but instead call `paint_next` which will update the graphics.

## Games
The following games have been implemented:
- Pong
- Flappy Bird (no gravity)
- Tetris
- Space Invaders