#Taken from
#https://developer.ridgerun.com/wiki/index.php/How_to_Capture_Frames_from_Camera_with_OpenCV_in_Python

import cv2
import sys

# Open the device at the ID 0
# Use the camera ID based on
# /dev/videoID needed
cap = cv2.VideoCapture(0)

#Check if camera was opened correctly
if not (cap.isOpened()):
    print("Could not open video device")
width = 640
height = 480

if len(sys.argv) > 1:
    if sys.argv[1] is "2":
        width = 960
        height = 720
    if sys.argv[1] is "3":
        width = 1280
        height = 720
    if sys.argv[1] is "4":
        width = 1920
        height = 1080
#Set the resolution
print("Setting resolution to {0}x{1}".format(width, height))
cap.set(cv2.CAP_PROP_FRAME_WIDTH, width)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, height)


# Capture frame-by-frame
while(True):
    ret, frame = cap.read()

    # Display the resulting frame
    cv2.imshow("preview",frame)
    cv2.imwrite("outputImage-{0}x{1}.jpg".format(width, height), frame)

    #Waits for a user input to quit the application
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
# When everything done, release the capture
cap.release()
cv2.destroyAllWindows()
