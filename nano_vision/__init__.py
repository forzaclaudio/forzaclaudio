import logging
import os

logging.basicConfig()
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

