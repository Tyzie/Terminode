from loguru import logger

import config

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