# INKRAFT - A Computer Graphics Project

**Made by Shaurya Dogra and Ritak Raj Pandey**

A simple Minecraft-inspired 3D block world written in Python using Pyglet and
OpenGL. It demonstrates core computer graphics concepts: 3D modelling,
geometric transformations, perspective and orthographic projection, texture
mapping, hidden surface removal (z-buffer, back-face culling), ray casting,
fog, alpha blending and drawing 2D UI from primitives.

The game opens on a start screen showing the project title and its authors,
with the world slowly rotating in the background. Click **START** (or press
Enter) to begin playing.

## Background Music

The game plays looping background music, with a mute button (speaker icon) in
the top right corner.

- By default it plays `music.wav`, an original 8-bit Game Boy style chiptune
  synthesised from square, triangle and noise waves by `make_music.py`.
  Run `python make_music.py` to regenerate it.
- To use your own track (for example Pokemon music you own), copy it into the
  game folder as `music.mp3`. It is played instead of `music.wav`.

## How to Run

Requires Python 3 and Pyglet 1.x (Pyglet 2 removed the legacy OpenGL functions
this project uses).

```shell
pip install "pyglet<2"
cd Minecraft
python main.py
```

Run `main.py` from inside the `Minecraft` folder so that `texture.png` is found.

## How to Play

### Start screen

- Click START or press Enter / Space: start the game
- ESC: quit

### Music

- M: mute / unmute the music (works anytime)
- Speaker icon (top right): click to mute / unmute while the mouse is free
  (on the start screen, or in game after pressing ESC)

### Moving

- W: forward
- S: back
- A: strafe left
- D: strafe right
- Mouse: look around
- Space: jump
- Tab: toggle flying mode

### Building

- Selecting type of block to create:
    - 1: brick
    - 2: grass
    - 3: sand
- Mouse left-click: remove block
- Mouse right-click: create block

### Quitting

- ESC: release mouse, then close window

## Credits

Based on [fogleman/Minecraft](https://github.com/fogleman/Minecraft) by
Michael Fogleman, used under the MIT License:

> Copyright (C) 2013 Michael Fogleman
>
> Permission is hereby granted, free of charge, to any person obtaining a copy of this software and associated documentation files (the "Software"), to deal in the Software without restriction, including without limitation the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies of the Software, and to permit persons to whom the Software is furnished to do so, subject to the following conditions:
>
> The above copyright notice and this permission notice shall be included in all copies or substantial portions of the Software.
>
> THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.
