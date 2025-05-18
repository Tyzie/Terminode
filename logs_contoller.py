from pathlib import Path
import sys

from loguru import logger

import config

if config.use_logs == True:
    log_path = Path('logs')
    log_path.mkdir(exist_ok=True)

    logger.remove()

    logger.add(
        log_path / "terminode_{time:YY-MM-DD}_{time:HH-mm}.log",
        rotation=config.log_max_size,
        retention="7 days",
        compression="zip",
        level="DEBUG",
        format="{time:YYYY-MM-DD HH:mm:ss} | {level} | {message}"
)
    logger.add(
        sys.stderr,
        format="{time:HH:mm:ss} | <level>{level}</level> | {message}"
)

def create_log(text: str, type: str):
    if config.use_logs == True:
        match type:
            case "debug":
                logger.debug(text)
            case "info":
                logger.info(text)
            case "suc":
                logger.success(text)
            case "warn":
                logger.warning(text)
            case "error":
                logger.error(text)
            case "critical":
                logger.critical(text)
    else:
        ...