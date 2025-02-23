import logging
from logging.handlers import RotatingFileHandler
import multiprocessing
from pathlib import Path
from datetime import datetime
from functools import wraps


def setup_logger(log_dir: str = "logs", verbose: bool = False) -> logging.Logger:
    """Setup a simple multiprocess-safe logger"""
    # Create logs directory if needed
    Path(log_dir).mkdir(exist_ok=True)

    # Create base logger
    logger = multiprocessing.get_logger()
    logger.setLevel(logging.DEBUG if verbose else logging.INFO)

    # Clear any existing handlers
    logger.handlers = []

    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - Process %(processName)s - %(levelname)s - %(message)s"
    )

    # Add rotating file handler
    log_file = Path(log_dir) / f"pharmacy_system_{datetime.now().strftime('%Y%m%d_%T')}.log"
    file_handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=3)  # 10MB
    file_handler.setFormatter(formatter)
    logger.addHandler(file_handler)

    # Add console handler
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    return logger, log_file


def with_logging(func):
    """Decorator to setup logging for worker processes"""

    @wraps(func)
    def wrapper(system, file_path, log_file, verbose):
        # Setup logging for this process
        logger = multiprocessing.get_logger()
        logger.handlers = []

        formatter = logging.Formatter(
            "%(asctime)s - Process %(processName)s - %(levelname)s - %(message)s"
        )

        file_handler = RotatingFileHandler(log_file, maxBytes=10 * 1024 * 1024, backupCount=3)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

        console_handler = logging.StreamHandler()
        console_handler.setFormatter(formatter)
        logger.addHandler(console_handler)

        logger.setLevel(logging.DEBUG if verbose else logging.INFO)

        # Update system's logger
        system.logger = logger

        return func(system, file_path)

    return wrapper
