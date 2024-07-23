from pathlib import Path
from unittest import mock
from unittest.mock import patch

import face_recognition
from nano_vision import commands


def test_learn_faces(tmp_path):
    """
    Ensure that command learns the faces from the default directory.
    """
    expected_datafile = "faces_data.pkl"
    training_data = tmp_path / "some_name.jpg"
    training_data.touch()
    expected_data = Path(expected_datafile)
    with patch.object(face_recognition, "load_image_file") as mock_load, patch.object(
        face_recognition, "face_encodings", return_value=[0, 1, 2]
    ) as mock_encoding:
        commands.learn_faces(training_dir=str(tmp_path.absolute()))
        mock_load.assert_called()
        mock_encoding.assert_called()
    assert expected_data.is_file()
    expected_data.unlink()


def test_learn_faces_saves_file(tmp_path):
    """
    Ensure faces data is saved to provided file.
    """
    expected_datafile = tmp_path / "expected_data.pkl"
    training_data = tmp_path / "some_name.jpg"
    training_data.touch()
    expected_data = Path(expected_datafile)
    with patch.object(face_recognition, "load_image_file") as mock_load, patch.object(
        face_recognition, "face_encodings", return_value=[0, 1, 2]
    ) as mock_encoding:
        commands.learn_faces(
            training_dir=str(tmp_path.absolute()),
            save_as=str(expected_datafile.absolute())
        )
        mock_load.assert_called()
        mock_encoding.assert_called()
    assert expected_datafile.is_file()
