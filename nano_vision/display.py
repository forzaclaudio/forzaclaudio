import cv2
import logging

logger = logging.getLogger(__name__)

class Overlays:
    def __init__(self):
        pass
    
    def fps(self, frame, fps = 0):
        font = cv2.FONT_HERSHEY_SIMPLEX
        cv2.putText(frame, "FPS: " + str(int(fps)), (11, 25), font, 0.5, (32, 32, 32), 4, cv2.LINE_AA)
        cv2.putText(frame, "FPS: " + str(int(fps)), (10, 25), font, 0.5, (240, 240, 240), 1, cv2.LINE_AA)

class Screen:
    def __init__(self):
        logger.debug("Initializing Screen...")
        self._width = 640
        self._height = 480

    def set_resolution(self, new_resolution = 1):
        if new_resolution == 1:
            self.width = 640
            self.height = 480
            return
        if new_resolution == 2:
            self.width = 960
            self.height = 720
            return
        if new_resolution == 3:
            self.width = 1280
            self.height = 720
            return
        if new_resolution == 4:
            self.width = 1920
            self.height = 1080
            return

    @property
    def width(self):
        logger.debug("Getting width... {}".format(self._width))
        return self._width

    @width.setter
    def width(self, value):
        logger.debug("Setting width to: {}".format(value))
        if value > 640 and value < 1920:
            raise ValueError("Width must be between 640 and 1920 px.")
        self._width = value

    @property
    def height(self):
        logger.debug("Getting height... {}".format(self._height))
        return self._height

    @height.setter
    def height(self, value):
        logger.debug("Setting height to: {}".format(value))
        if value > 640 and value < 1920:
            raise ValueError("Width must be between 480 and 1080 px.")
        self._height = value
