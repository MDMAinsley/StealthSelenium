import time
import random
import logging
from functools import wraps
from selenium.common.exceptions import WebDriverException

logger = logging.getLogger(__name__)

def retry_on_exception(max_retries=3, exceptions=(WebDriverException,), delay_range=(1, 3)):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for attempt in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except exceptions as e:
                    logger.warning("Retrying due to exception: %s (attempt %d)", e, attempt + 1)
                    time.sleep(random.uniform(*delay_range))
            raise
        return wrapper
    return decorator

def human_delay(min_sec=0.6, max_sec=2.0):
    time.sleep(random.uniform(min_sec, max_sec))

def type_like_human(element, text, min_delay=0.05, max_delay=0.15):
    for char in text:
        element.send_keys(char)
        time.sleep(random.uniform(min_delay, max_delay))
