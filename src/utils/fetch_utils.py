"""
Fetch utilities for NBA Projection System.
Handles API requests with retry logic and error handling.
Author: Edwin (Ed) Bleiler
"""
import time
import requests
from src.utils.logging import setup_logger

logger = setup_logger(__name__)


def fetch_with_retry(fetch_func, max_retries=3, delay=2, *args, **kwargs):
    """
    Execute a fetch function with retry logic.

    Args:
        fetch_func: Function to execute (from nba_api)
        max_retries: Maximum number of retry attempts
        delay: Delay between retries in seconds
        *args: Arguments to pass to fetch_func
        **kwargs: Keyword arguments to pass to fetch_func

    Returns:
        Result from fetch_func

    Raises:
        Exception: If all retries fail
    """
    last_exception = None

    for attempt in range(max_retries):
        try:
            result = fetch_func(*args, **kwargs)
            if attempt > 0:
                logger.info(f"Success on retry attempt {attempt + 1}")
            return result
        except Exception as e:
            last_exception = e
            logger.warning(f"Attempt {attempt + 1} failed: {str(e)}")

            if attempt < max_retries - 1:
                sleep_time = delay * (2 ** attempt)  # Exponential backoff
                logger.info(f"Retrying in {sleep_time} seconds...")
                time.sleep(sleep_time)
            else:
                logger.error(f"All {max_retries} attempts failed")

    raise last_exception


def safe_get_dict(obj, default=None):
    """
    Safely convert an object to dictionary.

    Args:
        obj: Object to convert (usually from nba_api)
        default: Default value if conversion fails

    Returns:
        dict or default value
    """
    if default is None:
        default = {}

    try:
        if hasattr(obj, 'get_dict'):
            return obj.get_dict()
        elif isinstance(obj, dict):
            return obj
        else:
            return default
    except Exception as e:
        logger.warning(f"Failed to convert object to dict: {str(e)}")
        return default
