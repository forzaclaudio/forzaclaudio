import cv2
import logging

from nano_vision import Screen, Video

logger = logging.getLogger(__name__)

video = Video()
screen = Screen()
res_code = Video.resolution_code()
screen.set_resolution(res_code)

cap = cv2.VideoCapture(0)
if not (cap.isOpened()):
    logger.error("Could not open video device e.g. /dev/video0")
    exit(1)

cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen.width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen.height)

while(True):
    ret, frame = cap.read()
    cv2.imshow("preview",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite("outputImage-{0}x{1}.jpg".format(screen.width, screen.height), frame)
        break

cap.release()
cv2.destroyAllWindows()
