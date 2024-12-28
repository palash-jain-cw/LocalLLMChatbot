from loguru import logger
import sys


def loguru_setup(
    logfile="./logs/logfile_{time:YYYY-MM-DD}.log",
    rotation="12:00",
):
    log_format = "{time} | {level} | {name} | {line} | {message}"
    logger.remove()
    logger.add(
        logfile,
        colorize=True,
        format=log_format,
        level="DEBUG",
    )
    logger.add(
        sys.stderr,
        format=log_format,
        colorize=True,
        backtrace=True,
        diagnose=True,
    )

    return logger
