import os
from .logger import get_logger

logger = get_logger("utils.files")

def remove_file(path: str):
    """
    Remove a file if it exists. Used as a background task to clean up temporary files.
    Args:
        path (str): The file path to remove.
    Returns:
        None
    """
    if os.path.exists(path):
        os.remove(path)
        logger.info(f"Deleted file: {path}")