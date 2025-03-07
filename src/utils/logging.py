import os
from sys import stdout

from loguru import logger


def configure_logger():
    logger.remove()

    log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", "logs"))
    os.makedirs(log_dir, exist_ok=True)

    logger.add(
        os.path.join(log_dir, "app.log"),
        rotation="10 MB",
        retention="7 days",
        level="INFO",
        format=(
            "{time:YYYY-MM-DD at HH:mm:ss} | {level} | "
            "{name}:{function}:{line} - {message}"
        ),
        backtrace=True,
        diagnose=True,
    )

    logger.add(
        stdout,
        level="INFO",
        format=(
            "<green>{time:YYYY-MM-DD at HH:mm:ss}</green> | "
            "<level>{level}</level> | "
            "<cyan>{name}</cyan>:<cyan>{function}</cyan>:<cyan>{line}</cyan> - "
            "<level>{message}</level>"
        ),
        backtrace=True,
        diagnose=True,
        colorize=True,
    )

    logger.info("Logger has been configured successfully.")


configure_logger()

__all__ = ["logger"]