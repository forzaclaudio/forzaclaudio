import cv2
from unittest.mock import MagicMock, patch

from nano_vision import commands, Video, Screen

def test_capture_image():
    """
    Ensure function instantiates video.
    """
    mock_cv = MagicMock()
    mock_cv.read.return_value = (None, None)
    with patch.object(Video, 'resolution_code', return_value=0) as mock_video, \
        patch.object(Screen, 'set_resolution') as mock_screen, \
        patch.object(cv2, 'VideoCapture', return_value=mock_cv) as mock_cv:
        commands.capture_image()
        mock_video.assert_called()
        mock_screen.assert_called()
        mock_cv.assert_called()
