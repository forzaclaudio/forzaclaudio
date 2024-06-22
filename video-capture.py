import cv2
import logging
from datetime import datetime
import time

from nano_vision import Screen
from nano_vision import Video
from nano_vision import Overlays


logger = logging.getLogger(__name__)

video = Video()
screen = Screen()
overlay = Overlays()
res_code = Video.resolution_code()
screen.set_resolution(res_code)

cap = cv2.VideoCapture(0)
if not (cap.isOpened()):
    logger.error("Could not open video device e.g. /dev/video0")
    exit(0)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen.width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen.height)

ts = time.time()
time_str = datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')

start = time.perf_counter()
frames_to_encode = []
while(cap.isOpened()):
    ret, frame = cap.read()
    frame_ts = time.perf_counter()-start
    logger.debug("Frame timestamp: {0}".format(frame_ts))
    overlay.elapsed_time(frame, frame_ts)
    if frame_ts > 10.0:
        break
    if ret==True:
        frames_to_encode.append(frame)
        cv2.imshow('frame',frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    else:
        break
cap.release()

video.save(screen, time_str, frames_to_encode, frame_ts)
cv2.destroyAllWindows()