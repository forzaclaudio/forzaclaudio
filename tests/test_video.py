import cv2
from pathlib import Path
import pytest
from unittest.mock import MagicMock, patch
import numpy as np

from nano_vision import Video, Screen


def test_video_without_path():
    """
    Ensure class provides a empty path.
    """
    v = Video()
    assert not v.path


def test_video_with_path(tmp_path):
    """
    Ensure class provides path attribute when the path exists.
    """
    v = Video(str(tmp_path.absolute()))
    assert isinstance(v.path, Path)
    assert v.path == tmp_path


@pytest.mark.parametrize(
    "test_path, expected_code",
    [
        ("test-640x480.mp4", 1),
        ("test-960x720.jpg", 2),
        ("test-1224x720.jpg", 3),
        ("test-1280x720.jpg", 4),
        ("test-1280x960.jpg", 5),
        ("test-1920x1080.mp4", 6),
    ],
)
def test_video_retrieves_resolution_from_path(test_path, expected_code):
    """
    If video path exists retrieves resolution from file.
    """
    v = Video("tests/test_data/{0}".format(test_path))
    assert v.resolution_code() == expected_code


def test_video_fails():
    """
    Resolution fails when trying to reproduce an invalid file.
    """
    v = Video("tests/test_data/{0}".format("test-broken.mp4"))
    with pytest.raises(ValueError):
        v.resolution_code()


def test_video_is_playing_flag():
    """
    Video play attribute is initially true and can be set to false.
    """
    v = Video()
    assert v.is_playing()
    v.play = False
    assert not v.is_playing()


def test_video_save_last_frame():
    """
    Video provides save last frame attribute.
    """
    v = Video()
    assert not v.save_last_frame
    v.save_last_frame = True
    assert v.save_last_frame

def _setup_video(tmp_path):
    screen = Screen()
    screen.set_resolution(2)
    v = Video()
    filename = tmp_path / "some_video.mp4"
    frame = cv2.imread("tests/test_data/test-960x720.jpg")
    v.add_frame(frame)
    return screen,v,filename

def test_video_provides_save_method(tmp_path):
    """
    Video class provides a save method.
    """
    screen, v, filename = _setup_video(tmp_path)
    assert not filename.is_file()
    video_writer = MagicMock()
    expected_filename = "some_filename"
    expected_fps = 1.0
    expected_width = 960
    expected_height = 720
    with patch.object(
        Video, "setup_encoding", return_value=(None, video_writer)
    ) as mock_encoding:
        v.save(screen, expected_filename, fps=expected_fps)
        mock_encoding.assert_called_with(
            expected_filename, expected_width, expected_height, expected_fps
        )

def test_save_method_writes_file(tmp_path):
    """
    Save method saves the given video
    """
    screen, v, filename = _setup_video(tmp_path)
    assert not filename.is_file()
    expected_fps = 1
    v.save(screen, str(filename.absolute()), fps=expected_fps)
    assert filename.is_file()

def test_video_initialize_timer():
    """
    Ensure video provides method to initialize its internal timer.
    """
    v = Video()
    with patch("time.perf_counter") as p:
        p.return_value = 1.0
        v.init_timer()
        assert p.called
    np.testing.assert_almost_equal(v.start_time, 1.0)


def test_video_timestamp():
    """
    Creates a current timestamp relative to the initialized internal timer.
    """
    v = Video()
    with patch("time.perf_counter") as p:
        p.return_value = 0.3
        ts = v.current_timestamp()
    np.testing.assert_almost_equal(ts, 0.3)


def test_video_provides_frames_to_encode():
    """
    Class contains a frames to encode attribute.
    """
    v = Video()
    assert not v.frames_to_encode


def test_video_provides_list_of_timestamps():
    """
    Class provides a list of frame timestamps.
    """
    v = Video()
    assert not v.ts_frames


def test_video_provides_method_to_add_frame():
    """
    Class provides a method to add frame.
    """
    frame = cv2.imread("tests/test/data/test-960x720.jpg")
    v = Video()
    v.add_frame(frame)
    assert len(v.frames_to_encode) == 1
    assert len(v.ts_frames) == 1
