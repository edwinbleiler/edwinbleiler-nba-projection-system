"""
Logging utilities for NBA Projection System.
Provides consistent logging configuration across all modules.
Author: Edwin (Ed) Bleiler
"""
import logging
import sys
from datetime import datetime


def setup_logger(name, level=logging.INFO):
    """
    Set up a logger with consistent formatting.

    Args:
        name: Logger name (usually __name__)
        level: Logging level (default: INFO)

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)

    # Avoid adding handlers multiple times
    if logger.hasHandlers():
        logger.handlers.clear()

    logger.setLevel(level)

    # Console handler
    handler = logging.StreamHandler(sys.stdout)
    handler.setLevel(level)

    # Format: timestamp - logger name - level - message
    formatter = logging.Formatter(
        '%(asctime)s - %(name)s - %(levelname)s - %(message)s',
        datefmt='%Y-%m-%d %H:%M:%S'
    )
    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger


def log_step(logger, message):
    """Log a major step in the pipeline."""
    logger.info("=" * 60)
    logger.info(message)
    logger.info("=" * 60)
