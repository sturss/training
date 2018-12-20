"""
    Module which creates and configures logger
"""
import logging


logger = logging.getLogger(__name__)

formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')

console_logger = logging.StreamHandler()
console_logger.setLevel(logging.DEBUG)
console_logger.setFormatter(formatter)

logger.addHandler(console_logger)
logger.setLevel(logging.DEBUG)