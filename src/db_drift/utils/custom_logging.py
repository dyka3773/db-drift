import logging
from logging.handlers import RotatingFileHandler
from pathlib import Path

LOGFILES_DIR_NAME = ".logs"


def setup_logger(name: str, level: int = logging.INFO) -> logging.Logger:
    """
    Set up a logger with a specific name and configuration.
    Note: This could also be used to modify an existing logger's configuration.

    Args:
        name (str): The name of the logger.
        level (int): The logging level. Default is logging.INFO.

    Returns:
        logging.Logger: The configured logger instance.
    """
    formatter = logging.Formatter(
        "%(asctime)s - %(threadName)s:%(thread)d - %(module)s:%(lineno)d - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    if not Path(LOGFILES_DIR_NAME).exists():
        Path(LOGFILES_DIR_NAME).mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger(name)

    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(logging.DEBUG)

    file_handler = RotatingFileHandler(
        filename=Path(LOGFILES_DIR_NAME) / f"{name}.log",
        maxBytes=5 * 1024 * 1024,  # 5 MB
        backupCount=5,  # Keep up to 5 backup log files
    )
    file_handler.setFormatter(formatter)
    file_handler.setLevel(logging.DEBUG)  # File handler logs everything from DEBUG and above

    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    console_handler.setLevel(level)  # Console handler logs from the specified level and above

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    logger.propagate = False  # Prevent log messages from being propagated to the root logger
    logger.debug(f"Logger '{name}' initialized with level {logging.getLevelName(level)}")

    return logger


def handle_verbose_logging() -> None:
    """Adjust the logging level based on the verbose flag."""
    logger = logging.getLogger("db-drift")
    for handler in logger.handlers:
        if isinstance(handler, logging.StreamHandler):
            handler.setLevel(logging.DEBUG)
