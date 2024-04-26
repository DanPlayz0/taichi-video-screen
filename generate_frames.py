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
  if not ret:
    break
  if frameId % 10 != 0: # Rendering only uses every 10th frame, so skip all others.
    frameId += 1
    continue
  converted_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
  with open(f"frames/{frameId}.json", "w") as f:
    f.write(json.dumps(converted_frame.tolist()))
    f.close()
  print(f"Processed frame {frameId}")
  frameId += 1
cap.release()
print("Processed all frames! You may now run player.py")