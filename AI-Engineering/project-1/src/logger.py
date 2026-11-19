import logging
import os

level_name = os.getenv("LOG_LEVEL", "INFO")
log_level = getattr(logging, level_name.upper(), logging.INFO)

logging.basicConfig(
    level=log_level,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
    datefmt="%Y-%m-%d %H-%M-%S",
)

def get_logger(name: str) -> logging.Logger:
    return logging.getLogger(name)