# app/logging_config.py

import logging
from app.config import LOG_LEVEL

def setup_logging():
    """
    Configures the root logger for the application.
    """
    # Get the numeric level from the string (e.g., "DEBUG" -> 10)
    log_level = logging.getLevelName(LOG_LEVEL.upper())

    # The format determines what information each log message contains.
    log_format = "%(asctime)s - %(levelname)s - %(name)s - %(message)s"

    # BasicConfig is a simple way to configure the root logger.
    logging.basicConfig(
        level=log_level,
        format=log_format,
        datefmt="%Y-%m-%d %H:%M:%S"
    )

    # You can also quiet down overly verbose libraries here if needed
    # logging.getLogger("httpx").setLevel(logging.WARNING)

    logging.info("Logging configured successfully.")