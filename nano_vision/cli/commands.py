import cv2
import logging

from nano_vision import Screen, Video

logger = logging.getLogger(__name__)

def _initialize(video_path):
    """
    Initialize video.
    """
    video = Video(video_path)
    res_code = video.resolution_code()
    screen = Screen()
    screen.set_resolution(res_code)
    return video, screen

def capture_image(video_path=None):
    """
    Capture an image from the given source.
    """
    video, _ = _initialize(video_path)
    if video.path:
        cap = cv2.VideoCapture(str(video.path.absolute()))
    else:
        print("Reading from stream")
        cap = cv2.VideoCapture(0)
    if not (cap.isOpened()):
        logger.error("Could not open video device e.g. /dev/video0")
        exit(1)

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


def extract_roi(video_path=None, save_last_frame=False):
    """
    Extract coordinates of region of interest (ROI).
    """
    video, screen = _initialize(video_path)
    video.save_last_frame=save_last_frame
    if video.path:
        cap = cv2.VideoCapture(str(video.path.absolute()))
    else:
        print("Reading from stream")
        cap = cv2.VideoCapture(0)
    if not (cap.isOpened()):
        logger.error("Could not open video device e.g. /dev/video0")
        exit(1)
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
    while(video.is_playing()):
        cv2.imshow('ROI Coordinates', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            if video.save_last_frame:
                cv2.imwrite("outputROI-{0}x{1}.jpg".format(screen.width, screen.height), frame)
            break

    cv2.destroyAllWindows()