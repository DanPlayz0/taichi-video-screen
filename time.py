import cv2
import json
cap = cv2.VideoCapture("video.mp4")
if not cap.isOpened():
  print("Video was unable to load. Try being in the same directory as the video & python file.")
  exit()
print('Video loaded.')
frameId = 0
while True:
  ret, frame = cap.read()
  if ret:
    converted_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    with open(f"frames/{frameId}.json", "w") as f:
      f.write(json.dumps(converted_frame.tolist()))
      f.close()
    frameId += 1