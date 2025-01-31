import logging
import os
import inspect


def setup_logger(name: str = None):
    """
    Sets up a logger with a given name. Logs are written to a file inside the logs directory and printed to the console.

    Args:
        name (str): Optional name for the logger. Defaults to the calling module's name.

    Returns:
        logging.Logger: Configured logger instance.
    """
    if name is None:
        # Get the name of the calling module
        frame = inspect.stack()[1]
        module = inspect.getmodule(frame[0])
        name = module.__name__ if module else "root"

    # Create a logs directory if it doesn't exist
    logs_dir = "logs"
    os.makedirs(logs_dir, exist_ok=True)

    # Set log file path
    log_file = os.path.join(logs_dir, f"{name}.log")

    logger = logging.getLogger(name)
    logger.setLevel(logging.DEBUG)  # Set base logging level to DEBUG

    # Console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)

    # File handler
    file_handler = logging.FileHandler(log_file)
    file_handler.setLevel(logging.DEBUG)

    # Formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    )
    console_handler.setFormatter(formatter)
    file_handler.setFormatter(formatter)

    # Add handlers to logger
    if not logger.hasHandlers():  # Avoid adding duplicate handlers
        logger.addHandler(console_handler)
        logger.addHandler(file_handler)

    return logger


def log_message(logger: logging.Logger, level: str, message: str):
    """
    Log a message with a given level using the provided logger.

    Args:
        logger (logging.Logger): Logger instance.
        level (str): The logging level (e.g., 'DEBUG', 'INFO', 'WARNING', 'ERROR', 'CRITICAL').
        message (str): The message to log.
    """
    level = level.upper()
    if level == "DEBUG":
        logger.debug(message)
    elif level == "INFO":
        logger.info(message)
    elif level == "WARNING":
        logger.warning(message)
    elif level == "ERROR":
        logger.error(message)
    elif level == "CRITICAL":
        logger.critical(message)
    else:
        logger.error(f"Invalid log level: {level}. Message: {message}")
