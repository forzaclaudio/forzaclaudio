import logging
import os

logging.basicConfig()
logging.root.setLevel(logging.NOTSET)

logger = logging.getLogger(__name__)

level = os.getenv("LOG_LEVEL")
if level:
    if level.lower() == 'info':
        logger.setLevel(logging.INFO)
    if level.lower() == 'warning':
        logger.setLevel(logging.WARNING)
    if level.lower() == 'debug':
        logger.setLevel(logging.DEBUG)
else:
    logger.setLevel(logging.INFO)

from .display import Overlays
from .display import Screen
from .machine_learning import read_face_data
from .input import Video
from .cli import commands
from .utils import generate_filename