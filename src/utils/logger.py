<<<<<<< HEAD
import logging
import os

os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    filename="logs/project.log",
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)

logger = logging.getLogger(__name__)
=======
# src/utils/logger.py
import logging
import os

# Create logs directory if it doesn't exist
os.makedirs("logs", exist_ok=True)

# Configure logger
logger = logging.getLogger("PriceMonitorLogger")
logger.setLevel(logging.DEBUG)

# File handler for logging
file_handler = logging.FileHandler("logs/app.log", encoding='utf-8')
file_handler.setLevel(logging.INFO)

# Console handler for real-time output
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)

# Formatter for both handlers
formatter = logging.Formatter('%(asctime)s | %(levelname)s | %(message)s')
file_handler.setFormatter(formatter)
console_handler.setFormatter(formatter)

# Add handlers to logger
logger.addHandler(file_handler)
logger.addHandler(console_handler)


if __name__ == "__main__":
    logger.info("Logger is working!")
>>>>>>> f0ba75326657d2188e7194689ed6a139e5d23b19
