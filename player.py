SCREEN_LEN_X = 256
SCREEN_LEN_Z = 144

import taichi as ti
ti.init(arch=ti.cpu)

window = ti.ui.Window('Test Square', (800, 800), fps_limit=60)
canvas = window.get_canvas()
scene = ti.ui.Scene()
camera = ti.ui.Camera()

camera.position(13.9,3,-33)
camera.lookat(14,3,0)

n = SCREEN_LEN_X * SCREEN_LEN_Z

@ti.kernel
def init_plane_mesh(vertices: ti.template(), len_z: int, len_x: int, y_offset: float):
  current_index = 0
  for x in range(len_x+1):
    for z in range(len_z+1):
      vertices[current_index] = [x*0.1+0.1,z*0.1+0.1,y_offset]
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


# 0.json, 1.json, ..., 907.json, 908.json
totalFrames = 908

import json
def init_frame_color(plane_colors: ti.template(), frameId: int):
  with open(f'frames/{frameId}.json') as f:
    pixels = json.loads(f.read())
    f.close()

  pixelNum = 0
  end = False
  for row in range(len(pixels)): # 144
    for col in range(len(pixels[row])): # 256
      cell = pixels[row][col]
      try:
        plane_colors[pixelNum] = (cell[0]/255, cell[1]/255, cell[2]/255)
      except:
        end = True
        print(plane_colors[pixelNum])
        print(pixelNum, type(cell), cell, cell[0]/255, cell[1]/255, cell[2]/255)
      pixelNum+=1
      if end:
        break
    if end:
      break


t = 0.0

paused = True
frameId = 100
timeout = 0
init_frame_color(plane_colors, frameId)
# print(plane_colors)

while window.running:
  if window.get_event(ti.ui.RELEASE):
    if window.event.key == ti.ui.SPACE:
      paused = not paused
    elif window.event.key == ti.ui.BACKSPACE:
      print(camera.curr_lookat)
      print(camera.curr_position)

  init_frame_color(plane_colors, frameId%totalFrames)
  frameId += 10

  camera.track_user_inputs(window, movement_speed=0.06, hold_key=ti.ui.LMB)
  scene.set_camera(camera)
  # scene.ambient_light((0.9, 0.9, 0.9))
  # scene.point_light(pos=(3,3,1), color=(1,0.9,0.5))
  # scene.point_light(pos=(-3,3,1), color=(1,0.9,0.5))
  # scene.mesh(plane_vertices, indices=plane_indices, color=(14/255, 65/255, 46/255), two_sided=True, show_wireframe=False)
  # scene.particles(plane_vertices, radius=0.1, color=(14/255, 65/255, 46/255))
  scene.particles(plane_vertices, radius=0.1, per_vertex_color=plane_colors)
  canvas.scene(scene)
  window.show()