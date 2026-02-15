import logging
import sys
from typing import ClassVar


class CustomFormatter(logging.Formatter):

    grey: str = "\x1b[38;20m"
    green: str = "\x1b[32;20m"
    yellow: str = "\x1b[33;20m"
    blue: str = "\x1b[34;20m"
    red: str = "\x1b[31;20m"
    bold_red: str = "\x1b[31;1m"
    reset: str = "\x1b[0m"
    FORMAT: ClassVar[str] = (
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s (%(filename)s:%(lineno)d)"
    )

    FORMATS: ClassVar = {
        logging.DEBUG: grey + FORMAT + reset,
        logging.INFO: green + FORMAT + reset,
        logging.WARNING: yellow + FORMAT + reset,
        logging.ERROR: red + FORMAT + reset,
        logging.CRITICAL: bold_red + FORMAT + reset,
    }

    def format(self, record):
        log_fmt = self.FORMATS.get(record.levelno)
        formatter = logging.Formatter(log_fmt, datefmt="%Y-%m-%d %H:%M:%S")
        return formatter.format(record)


logging_handler = logging.StreamHandler(sys.stdout)
logging_handler.setFormatter(CustomFormatter())
