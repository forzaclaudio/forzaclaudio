import cv2
from unittest.mock import MagicMock, patch
from pathlib import Path
import pytest

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

def test_capture_image():
    """
    Ensure function reads from video when a path is provided.
    """
    m = MagicMock()
    m.read.return_value = (None, None)
    filepath = Path("tests/test_data/test-640x480.mp4")
    with patch("cv2.VideoCapture", return_value=m) as vc:
        with pytest.raises(ValueError):
            commands.capture_image(video_path=str(filepath.absolute()))
        assert vc.called_with(filepath.absolute())
