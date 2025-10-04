import os

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
        print(f"[INFO] Deleted file: {path}")