SCREEN_LEN_X = 144
SCREEN_LEN_Z = 255

import taichi as ti
ti.init(arch=ti.cpu)

window = ti.ui.Window('Test Square', (800, 800))
canvas = window.get_canvas()
scene = ti.ui.Scene()
camera = ti.ui.Camera()

camera.position(13.9,3,-33)
camera.lookat(14,3,0)

n = SCREEN_LEN_X * SCREEN_LEN_Z

@ti.kernel
def init_plane_mesh(vertices: ti.template(), len_y: int, len_x: int, z_offset: float):
  current_index = 0
  for x in range(len_x+1):
    for y in range(len_y+1):
      vertices[current_index] = [y*0.1+0.5,x*-0.1+0.5,z_offset]
      current_index += 1

@ti.kernel
def init_mesh_indices(indices: ti.template(), len_z: int, len_x: int):
  current_index = -6
  rowLength = len_x+1
  for x in range(len_x):
    for z in range(len_z):
      current_index += 6
      indices[current_index] = z * rowLength + x
      indices[current_index + 1] = z * rowLength + x + 1
      indices[current_index + 2] = (z + 1) * rowLength + x

      indices[current_index + 3] = z * rowLength + x + 1
      indices[current_index + 4] = (z + 1) * rowLength + x + 1
      indices[current_index + 5] = (z + 1) * rowLength + x
  

plane_vertices = ti.Vector.field(3, dtype=float, shape = (SCREEN_LEN_Z+1) * (SCREEN_LEN_X+1))
plane_indices = ti.field(dtype=int, shape = 6*n)
plane_colors = ti.Vector.field(3, dtype=float, shape = (SCREEN_LEN_Z+1) * (SCREEN_LEN_X+1))
init_plane_mesh(plane_vertices, SCREEN_LEN_Z, SCREEN_LEN_X, 0)
init_mesh_indices(plane_indices, SCREEN_LEN_Z, SCREEN_LEN_X)


frames = []
import json

def init_frame_pixels(frameId: int):
  with open(f'frames/{frameId}.json') as f:
    pixels = json.loads(f.read())
    f.close()
  
  frame = []
  for row in range(len(pixels)): # 144
    for col in range(len(pixels[row])): # 256
      cell = pixels[row][col]
      frame.append((cell[0]/255, cell[1]/255, cell[2]/255))
  frames.append(frame)

for i in range(0, 30, 10):
  print("Init frame", i)
  init_frame_pixels(i)

from threading import Thread
def cache_thread():
  for i in range(30,5300, 10):
    print("post-init frame", i)
    init_frame_pixels(i)

caching_thread = Thread(target=cache_thread)
caching_thread.start()

def update_frame(plane_colors: ti.template(), frameId: int):
  frame = frames[frameId%len(frames)]
  for i in range(len(frame)):
    plane_colors[i] = frame[i]

t = 0.0

paused = True
frameId = 1
timeout = 0
update_frame(plane_colors, frameId)
# print(plane_colors)

while window.running:
  if window.get_event(ti.ui.RELEASE):
    if window.event.key == ti.ui.SPACE:
      paused = not paused
    elif window.event.key == ti.ui.BACKSPACE:
      print(camera.curr_lookat)
      print(camera.curr_position)
    # elif window.event.key == ti.ui.RIGHT:
    #   frameId += 10
    #   update_frame(plane_colors, frameId%totalFrames)
    # elif window.event.key == ti.ui.LEFT:
    #   frameId -= 10
    #   update_frame(plane_colors, frameId%totalFrames)
  # frameId += 10

  if not paused:
    frameId = (frameId + 1) % len(frames)
    update_frame(plane_colors, frameId)

  camera.track_user_inputs(window, movement_speed=0.06, hold_key=ti.ui.LMB)
  scene.set_camera(camera)
  scene.ambient_light((0.9, 0.9, 0.9))
  # scene.point_light(pos=(3,3,1), color=(1,0.9,0.5))
  # scene.point_light(pos=(-3,3,1), color=(1,0.9,0.5))
  # scene.mesh(plane_vertices, indices=plane_indices, color=(14/255, 65/255, 46/255), two_sided=True, show_wireframe=False)
  # scene.particles(plane_vertices, radius=0.1, color=(14/255, 65/255, 46/255))
  scene.particles(plane_vertices, radius=0.1, per_vertex_color=plane_colors)
  canvas.scene(scene)
  window.show()
