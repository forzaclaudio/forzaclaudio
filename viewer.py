import cv2
from nano_vision import Screen
from nano_vision import Video
from nano_vision import Overlays

video = Video()
screen = Screen()
overlay = Overlays()

res_code = Video.resolution_code()
screen.set_resolution(res_code)

cap = cv2.VideoCapture(0)
if not (cap.isOpened()):
    print("Could not open video device")


cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen.width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen.height)

while(True):
    timer = cv2.getTickCount()
    ret, frame = cap.read()
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    overlay.fps(frame, fps)
    cv2.imshow("preview",frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        cv2.imwrite("outputImage-{0}x{1}.jpg".format(screen.width, screen.height), frame)
        break

cap.release()
cv2.destroyAllWindows()
