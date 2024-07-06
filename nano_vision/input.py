import cv2
import re
import logging
import subprocess

from pathlib import Path

logger = logging.getLogger(__name__)

class Video:
    def __init__(self, src_path=None):
        """Initialize the video instance."""
        self._path = self._validated_path(src_path)
        self._play = True
        self._save_last_frame = False
    
    @property
    def save_last_frame(self):
        """
        Return the flag that indicates if last frame is saved.
        """
        return self._save_last_frame

    @save_last_frame.setter
    def save_last_frame(self, new_state):
        """
        Set the flag that indicates if last frame is saved.
        """
        self._save_last_frame = new_state

    @property
    def play(self):
        """
        Return the flag that indicates that video is playing.
        """
        return self._play

    @play.setter
    def play(self, new_state):
        """
        Set the flag that indicates that video is playing.
        """
        self._play = new_state

    def is_playing(self):
        """
        Return playing status.
        """
        return self._play
    @property
    def path(self):
        """
        Return the path of the video.
        """
        return self._path

    @path.setter
    def path(self, new_path):
        """
        Set the path for the video.
        """
        self._path = self._validated_path(new_path)

    def _validated_path(self, input_path):
        """If path exists assign it to instance."""
        if input_path:
            path = Path(input_path)
            if path.is_file:
                return path
        return None

    def resolution_code(self):
        """
        Return the resolution of the current video source.
        """
        if not self._path:
            try:
                proc = subprocess.Popen(["v4l2-ctl", "--all"], stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            except FileNotFoundError as e:
                logger.error(str(e))
            try:
                outs, errs = proc.communicate()
            except Exception as e:
                logger.error(str(e))
                exit(1)
            logger.debug("Captured output: {}".format(outs))
            logger.debug("Captured errors: {}".format(errs))
            m = re.search("\d.*/\d*", outs.decode("utf-8"))
            if not m:
                logger.error("Unable to find video resolution values")
                exit(1)
            values = m.group(0).split("/")
            width = values[0]
            height = values[1]
        else:
            cap = cv2.VideoCapture(str(self._path.absolute()))
            ret, frame = cap.read()
            if not ret:
                msg = "Unable to read file: {0}".format(self._path.absolute())
                logger.error(msg)
                raise ValueError(msg)
            width = frame.shape[1]
            height = frame.shape[0]
        logger.debug("width found: {0}, height found: {1}".format(width, height))
        if int(width) == 640 and int(height) == 480:
            return 1
        if int(width) == 960 and int(height) == 720:
            return 2
        if int(width) == 1224 and int(height) == 720:
            return 3
        if int(width) == 1280 and int(height) == 720:
            return 4
        if int(width) == 1280 and int(height) == 960:
            return 5
        if int(width) == 1920 and int(height) == 1080:
            return 6
        return 0

    def setup_encoding(self, time_str, width, height, fps):
        logger.debug("Received time string: {0} Width: {1} Height: {2}".format(
            time_str, width, height)
        )
        fourcc = cv2.VideoWriter_fourcc(*"x264")
        out = cv2.VideoWriter(
            "video-{0}x{1}-{2}.mp4".format(width, height, time_str),
            fourcc, fps, (width, height))

        return fourcc, out
        
    def save(self, screen, time_str, frames_to_encode, frame_ts, fps=None):
        """
        screen has the dimensions of the frame to save.
        time_str will be used to name the video.
        frames_to_encode is the list of frames to encode
        frame_ts is the timestamp of the last processed frame
        frame_ts is ignored is fps is defined!
        """
        num_frames =  len(frames_to_encode)
        logger.info("Frames to encode: {0}".format(num_frames))
        if fps:
            fourcc, out = self.setup_encoding(time_str, screen.width, screen.height, fps)
        else:
            fps = num_frames/frame_ts
            logger.debug("FPS: {0:.3f}", fps)
            fourcc, out = self.setup_encoding(time_str, screen.width, screen.height, num_frames/frame_ts)
        logger.info("Saving video...")
        for i in range(num_frames):
            logger.debug("Writing frame: {0}".format(i))
            out.write(frames_to_encode[i])
        logger.info("Done!")
        out.release()