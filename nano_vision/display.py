import logging

import cv2
import numpy as np

logger = logging.getLogger(__name__)

RGB_WHITE = (255, 255, 255)

class Overlays:
    def __init__(self):
        self._font = cv2.FONT_HERSHEY_SIMPLEX
        self._text_bkg = (32, 32, 32)
        self._text_fg = (240, 240, 240)
        self._text_fg_origin = (11, 25)
        self._text_bg_origin = (10, 25)
        self._font_scale = 0.5
        self._line_thickness = 2
    
    def roi(self, frame, top, right, bottom, left, color, text=None):
        """
        Add a rectangle and label it with the given text.
        """
        cv2.rectangle(frame, (right, top), (left, bottom), color, self._line_thickness)
        if not text:
            return
        cv2.putText(frame, text, (left, top - 6), self._font, self._font_scale, RGB_WHITE, self._line_thickness)

    def mask(self, frame, top, right, bottom, left,  color):
        """
        Add a rectangle to the provided frame.
        """
        cv2.rectangle(frame, (right, top), (left, bottom), color, cv2.FILLED)

    def add_video(self, frame, video_to_add):
        """
        Add image to the current frame.
        """
        tempImg = frame.copy()
        tempImg [0:video_to_add.shape[0], 0:video_to_add.shape[1]] = video_to_add
        return tempImg


    def blend(self, img_1, img_2):
        """
        Return blended image

        returned_img = img_1*alpha + img_2 * beta + gamma
        """
        alpha = 1.0
        beta = 0.4
        gamma = 1.0
        return cv2.addWeighted(img_1, alpha, img_2, beta, gamma)

    def blur(self, frame, top, right, bottom, left):
        """
        Blurs a circular region.

        0        X
            0 1
            2 3
        Y
        (top, right) = 0
        (bottom,left) = 3
        """
        logger.debug(
            "Coordinates for blurring: top: {0}, right: {1}, bottom: {2}, left: {3}".format(
                top, right, left, bottom))
        x=top
        y=right
        w=bottom-top
        h=left-right
        tempImg = frame.copy()
        maskShape = (frame.shape[0], frame.shape[1], 1)
        mask = np.full(maskShape, 0, dtype=np.uint8)
        tempImg [y:y+h, x:x+w] = cv2.blur(tempImg [y:y+h, x:x+w] ,(25,25))
        cv2.circle(mask, ( int((x + x + w )/2), int((y + y + h)/2 )), int (h / 2), (255), -1)

        mask_inv = cv2.bitwise_not(mask)
        img1_bg = cv2.bitwise_and(frame, frame, mask = mask_inv)
        img2_fg = cv2.bitwise_and(tempImg, tempImg, mask = mask)
        return cv2.add(img1_bg, img2_fg)

    def fps(self, frame, fps = 0):
        """
        Collect fps by executing the following:
        timer = cv2.getTickCount()
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer)
        """
        text = "FPS: {0}".format(str(int(fps)))
        logger.debug(text)
        self._write_string(frame, text)

    def total_faces(self, frame, faces):
        text = "Total Faces Detected: {0}".format(faces)
        logger.debug(text)
        second_num_line = 1
        self._write_string(frame, text, second_num_line)

    def elapsed_time(self, frame, timestamp):
        text = "Elapsed time[s] {0:.3f}".format(timestamp)
        logger.debug(text)
        first_num_line = 0
        self._write_string(frame, text, first_num_line)

    def _write_string(self, frame, text, num_line):
        space_between_text = 20
        cv2.putText(frame, text, (self._text_fg_origin[0], self._text_fg_origin[1]+space_between_text*num_line), self._font, self._font_scale, self._text_bkg, 4, cv2.LINE_AA)
        cv2.putText(frame, text, (self._text_bg_origin[0], self._text_bg_origin[1]+space_between_text*num_line), self._font, self._font_scale, self._text_fg, 1, cv2.LINE_AA)

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
            self.width = 1224
            self.height = 720
            return
        if new_resolution == 4:
            self.width = 1280
            self.height = 720
            return
        if new_resolution == 5:
            self.width = 1280
            self.height = 960
            return
        if new_resolution == 6:
            self.width = 1920
            self.height = 1080
            return
        raise ValueError("{0} is not a valid resolution code".format(new_resolution))

    @property
    def width(self):
        logger.debug("Getting width... {}".format(self._width))
        return self._width

    @width.setter
    def width(self, value):
        logger.debug("Setting width to: {}".format(value))
        if value < 640 and value > 1920:
            raise ValueError("Width must be between 640 and 1920 px.")
        self._width = value

    @property
    def height(self):
        logger.debug("Getting height... {}".format(self._height))
        return self._height

    @height.setter
    def height(self, value):
        logger.debug("Setting height to: {}".format(value))
        if value < 480 and value > 1920:
            raise ValueError("Width must be between 480 and 1080 px.")
        self._height = value
