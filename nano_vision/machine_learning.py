import logging
import pickle
from pathlib import Path

logger = logging.getLogger(__name__)

def read_face_data(path_to_data):
    """
    Read names and encodings stored in data_path.
    """
    data_path = Path(path_to_data)
    if data_path.is_file():
        with open(Path(data_path).absolute(),'rb') as f:
            Names = pickle.load(f)
            Encodings = pickle.load(f)
            logger.debug(
                "Loaded file with trained data: '{0}'".format(data_path.absolute())
            )
    else:
        logger.error(
            "Unable to open file with trained data: '{0}'".format(data_path.absolute())
        )
        exit(1)
    return Names, Encodings