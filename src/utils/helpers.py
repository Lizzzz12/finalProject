import random
import time
from typing import List, Dict, Any

def random_delay(min_sec: float = 1.0, max_sec: float = 3.0):
    """Random delay between requests to avoid detection"""
    time.sleep(random.uniform(min_sec, max_sec))

def rotate_user_agent() -> str:
    """Return a random user agent string"""
    agents = [
        'Mozilla/5.0 (Windows NT 10.0; Win64; x64)',
        'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7)',
        'Mozilla/5.0 (Linux; Android 10; SM-G960U)'
    ]
    return random.choice(agents)