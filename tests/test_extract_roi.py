import cv2
from unittest.mock import MagicMock, patch

from nano_vision import commands, Video, Screen

def test_extract_roi():
    """
    Ensure function extracts roi.
    """
    mock_cv = MagicMock()
    mock_cv.read.return_value = (None, None)
    with patch.object(Video, 'resolution_code', return_value=0) as mock_video, \
        patch.object(Screen, 'set_resolution') as mock_screen, \
        patch.object(Video, 'is_playing', return_value=False) as mock_play, \
        patch.object(Video, 'is_playing', return_value=False) as mock_play, \
        patch.object(cv2, 'namedWindow') as mock_named_window, \
        patch.object(cv2, 'VideoCapture', return_value=mock_cv) as mock_video_capture:
        commands.extract_roi()
        mock_video.assert_called()
        mock_play.assert_called()
        mock_screen.assert_called()
        mock_video_capture.assert_called()
        mock_named_window.assert_called_with("ROI Coordinates")