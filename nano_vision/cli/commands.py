import cv2
import logging
from pathlib import Path

from nano_vision import Screen, Video

logger = logging.getLogger(__name__)

def image_capture(video_path=None):
    """
    Capture an image from the given source.
    """
    video = Video(video_path)
    res_code = video.resolution_code()
    # screen = Screen()
    # screen.set_resolution(res_code)
    if video.path:
        cap = cv2.VideoCapture(str(video.path.absolute()))
    else:
        print("Reading from stream")
        cap = cv2.VideoCapture(0)
    if not (cap.isOpened()):
        logger.error("Could not open video device e.g. /dev/video0")
        exit(1)

    # cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen.width)
    # cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen.height)

    while(cap.isOpened()):
        ret, frame = cap.read()
        if not ret:
            break
        cv2.imshow("preview",frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            cv2.imwrite("outputImage-{0}x{1}.jpg".format(frame.shape[1], frame.shape[0]), frame)
            break

    cap.release()
    cv2.destroyAllWindows()
