import logging

default_formatter = logging.Formatter("%(asctime)s [%(levelname)s] %(message)s")
default_level = logging.INFO

def get_logger(name: str = "app") -> logging.Logger:
    """
    Creates and returns a logger with a file handler and optional console output.
    """
    logger = logging.getLogger(name)
    if logger.handlers:
        # If the logger already has handlers, do not add them again
        return logger

    logger.setLevel(default_level)

    # File handler
    # log_file = "logs/app.log"
    # file_handler = logging.FileHandler(log_file)
    # file_formatter = default_formatter
    # file_handler.setFormatter(file_formatter)
    # logger.addHandler(file_handler)

    # Console handler (optional)
    console_handler = logging.StreamHandler()
    console_formatter = default_formatter
    console_handler.setFormatter(console_formatter)
    logger.addHandler(console_handler)

    return logger
