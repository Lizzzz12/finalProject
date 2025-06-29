# src/utils/helpers.py

import time
import random

def retry(func, retries: int = 3, backoff: float = 1.0, *args, **kwargs):
    """
    Retry a function up to `retries` times, waiting backoff*i seconds between attempts.
    """
    for i in range(1, retries + 1):
        try:
            return func(*args, **kwargs)
        except Exception as e:
            if i == retries:
                raise
            wait = backoff * i
            time.sleep(wait)

def random_delay(min_s: float = 0.5, max_s: float = 2.0):
    """
    Sleep for a random duration between min_s and max_s to avoid triggering anti-bot.
    """
    time.sleep(random.uniform(min_s, max_s))
