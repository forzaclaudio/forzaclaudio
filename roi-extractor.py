import logging
import time

import cv2
import numpy as np

from nano_vision import Screen
from nano_vision import Video
from nano_vision import Overlays

logger = logging.getLogger(__name__)

video = Video()
screen = Screen()
overlay = Overlays()

#res_code = Video.resolution_code()
screen.set_resolution(4)

cap = cv2.VideoCapture("downloads/20240629_132553.mp4")
if not (cap.isOpened()):
    print("Could not open video device")

cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen.width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen.height)

def click_event(event, x, y, flags, params):
    if event == cv2.EVENT_LBUTTONDOWN:
        print('Left Click')
        print(f'({x},{y})')
        cv2.putText(frame, f'({x},{y})', (x, y),   cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 0, 0), 2)
        cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)
    if event == cv2.EVENT_RBUTTONDOWN:
        print('Right Click')
        print(f'({x},{y})')
        cv2.putText(frame, f'({x},{y})', (x, y),
        cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)
        cv2.circle(frame, (x, y), 3, (0, 0, 255), -1)

ret, frame = cap.read()
cv2.namedWindow('ROI Coordinates')
cv2.setMouseCallback('ROI Coordinates', click_event)
cap.release()
while(True):
    cv2.imshow('ROI Coordinates', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        #cv2.imwrite("outputImage-{0}x{1}.jpg".format(screen.width, screen.height), frame)
        break

cv2.destroyAllWindows()
