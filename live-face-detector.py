import logging
import time
from datetime import datetime

import cv2
import face_recognition
import numpy as np

from nano_vision import Overlays, Screen, Video, read_face_data

logger = logging.getLogger(__name__)

screen = Screen()
video = Video()
overlays = Overlays()
res_code = Video.resolution_code()
screen.set_resolution(res_code)
SAVE_RECORDING = False

Names, Encodings = read_face_data("train.pkl")

if screen.height == 480:
    scale = 1.0
else:
    scale = 0.25

up_points = (screen.width, screen.height)
cap = cv2.VideoCapture(0)
ret, frame = cap.read()

ts = time.time()
time_str = datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')

facePositions = face_recognition.face_locations(frame)
allEncodings = face_recognition.face_encodings(frame,facePositions)
start = time.perf_counter()
frames_to_encode = []
while cap.isOpened():
    ret, frame = cap.read()
    frame_ts = time.perf_counter()-start
    if ret == False:
        logger.error("Unable to read camera")
        break
    rgb = cv2.cvtColor(frame,cv2.COLOR_BGR2RGB)
    rgb = cv2.resize(rgb, (0, 0), fx=scale, fy=scale)

    facePositions = face_recognition.face_locations(rgb)
    allEncodings = face_recognition.face_encodings(rgb,facePositions)
    img = cv2.cvtColor(rgb,cv2.COLOR_RGB2BGR)
    blk = np.zeros(frame.shape, np.uint8)

    people = []
    count = 0
    for (top,right,bottom,left), face_encoding in zip(facePositions,allEncodings):
        name = 'Unknown Person'
        matches = face_recognition.compare_faces(Encodings, face_encoding)
        if True in matches:
            first_match_index = matches.index(True)
            color = (0,255,0)
            name = Names[first_match_index]
            people.append(name)
        else:
            color = (0,0,255)
        count += 1
        overlays.roi(frame, int(top/scale), int(right/scale), int(bottom/scale), int(left/scale), color, text=name)
        frame = overlays.blur(frame, int(left/scale), int(top/scale), int(right/scale), int(bottom/scale))
        overlays.mask(blk, int(top/scale), int(right/scale), int(bottom/scale), int(left/scale), color)

    logger.info('{} People Detected. Recognized people: {}'.format(count,people))
    out = overlays.blend(frame, blk)
    overlays.total_faces(out, count)
    overlays.elapsed_time(out, frame_ts)

    cv2.imshow('Face Detector', out)
    if SAVE_RECORDING:
        frames_to_encode.append(frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
if SAVE_RECORDING:
    video.save(screen, time_str, frames_to_encode, frame_ts)
cv2.destroyAllWindows()
