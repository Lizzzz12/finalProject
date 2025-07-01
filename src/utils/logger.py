# -------------------- src/utils/logger.py --------------------
import logging
import os

os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    filename="logs/project.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
logger = logging.getLogger(__name__)
