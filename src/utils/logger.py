# src/utils/logger.py

import logging
import os

def get_logger(name: str) -> logging.Logger:
    """
    Create or retrieve a logger that writes to logs/app.log.
    """
    log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "logs"))
    os.makedirs(log_dir, exist_ok=True)
    log_path = os.path.join(log_dir, "app.log")

    logger = logging.getLogger(name)
    if not logger.handlers:
        logger.setLevel(logging.INFO)
        handler = logging.FileHandler(log_path, encoding="utf-8")
        fmt = logging.Formatter("%(asctime)s %(levelname)s [%(name)s] %(message)s")
        handler.setFormatter(fmt)
        logger.addHandler(handler)
    return logger
