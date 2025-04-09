# backend/app/core/logger.py
import sys
from loguru import logger
from app.core.config import settings

# Remove default handler
logger.remove()

# Add console handler
logger.add(
    sys.stderr,
    level=settings.LOG_LEVEL.upper(),
    format="<green>{time:YYYY-MM-DD HH:mm:ss}</green> | <level>{level: <8}</level> | <cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - <level>{message}</level>"
)

# Add file handler if LOG_FILE is set in config
if settings.LOG_FILE:
    logger.add(
        settings.LOG_FILE,
        level=settings.LOG_LEVEL.upper(),
        rotation="10 MB",  # Rotate log file when it reaches 10 MB
        retention="7 days", # Keep logs for 7 days
        compression="zip", # Compress rotated files
        format="{time:YYYY-MM-DD HH:mm:ss} | {level: <8} | {name}:{function}:{line} - {message}"
    )

# Example usage (can be imported elsewhere):
# from app.core.logger import logger
# logger.info("This is an info message.")
# logger.debug("This is a debug message.") 