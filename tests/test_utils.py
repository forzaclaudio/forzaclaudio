import time
from datetime import datetime

import pytest
from nano_vision.utils import generate_filename


@pytest.mark.parametrize(
    "parameters,expected", [
        ((None, None, None, None), "video.mp4"),
        (("some-prefix", None, None, None), "some-prefix.mp4"),
        (("some-prefix", 640, 480, None), "some-prefix-640x480.mp4"),
    ]
)
def test_generate_filename(parameters, expected):
    """
    Utils provide method to generate filename.
    """
    assert (
        generate_filename(prefix=parameters[0], width=parameters[1], height=parameters[2], timestamp=parameters[3])
        == expected
    )

def test_generate_filename():
    """
    Generate filename with timestamp.
    """
    ts = time.time()
    expected_str = "video-"
    expected_str += datetime.fromtimestamp(ts).strftime('%Y-%m-%d_%H:%M:%S')
    expected_str += ".mp4"
    assert generate_filename(timestamp=ts) == expected_str
