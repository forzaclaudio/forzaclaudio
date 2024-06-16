#Taken from
#https://developer.ridgerun.com/wiki/index.php/How_to_Capture_Frames_from_Camera_with_OpenCV_in_Python

import cv2
from nano_vision import Screen, Overlays

cap = cv2.VideoCapture(0)
if not (cap.isOpened()):
    print("Could not open video device")
screen = Screen()
screen.set_resolution(2)
overlay = Overlays()
print("Setting resolution to {0}x{1}".format(screen.width, screen.height))

cap.set(cv2.CAP_PROP_FRAME_WIDTH, screen.width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, screen.height)

while(True):
    timer = cv2.getTickCount()
    ret, frame = cap.read()
    fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
    overlay.fps(frame, fps)
    cv2.imshow("preview",frame)
    cv2.imwrite("outputImage-{0}x{1}.jpg".format(screen.width, screen.height), frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
cap.release()
cv2.destroyAllWindows()
