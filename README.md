# Taichi Video Screen

This project is a proof of concept to project a 480p video onto particles to give an illiousion of a screen.

Currently uses aprox 3.3 GB of RAM to cache every 10th frame of a 480p video.

## How do I use this?

1. Download the repository, via the zip file or `git clone https://github.com/DanPlayz0/taichi-video-screen.git`
2. Extract the zip and open a terminal (or command prompt) inside that folder.
3. Once your in that folder, run `python3 generate_frames.py`
4. If you don't already have [taichi lang](https://www.taichi-lang.org/) installed, install it. (`pip3 install taichi`)
4. Once it exits, you may run `python3 player.py`
5. When it opens, you can click and hold to move around the camera, use WASD to move in space.
6. Once you've positioned however you'd like the camera to sit. Hit the `SPACE` to play or pause.

## Controls

| Action         | Key             |
| -------------- | --------------- |
| Pause/Play     | Space           |
| Previous Frame | Left Arrow Key  |
| Next Frame     | Right Arrow Key |
| Move Forward   | W               |
| Move Backward  | S               |
| Move Left      | A               |
| Move Right     | D               |
| Move Up        | E               |
| Move Down      | Q               |

## Credits

- [Taichi Lang](https://www.taichi-lang.org/)
- [video.mp4](https://www.youtube.com/watch?v=dQw4w9WgXcQ)
