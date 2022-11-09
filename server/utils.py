import logging
from dataclasses import dataclass
from typing import List


@dataclass
class Config:
    admissible_tokens: List[str]
    path_to_database: str


class STATUS:
    OK = 200
    CREATED = 201
    UPDATED = 202
    GENERIC_ABORT = 400
    INVALID_VERSION = 401
    FORBIDDEN = 403  # used when company token is invalid
    NOT_FOUND = 404  # used when particular element requested by ID is not available
    NOT_AVAILABLE = 405  # used when multiple requested elements are not
    FAIL = 406


@dataclass
class Data:
    temperature: float
    humidity: float
    timestamp: float
    room: str

    @property
    def data_to_row(self) -> str:
        return f"{self.timestamp};{self.room};{self.temperature};{self.humidity}"

    @property
    def data_keys(self) -> str:
        return "timestamp;room;temperature;humidity"


def get_logger(logger_name):
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger(logger_name)
    formatter = logging.Formatter(
        "%(asctime)s logger:%(name)s:%(levelname)s :\t%(message)s",
        datefmt="%Y-%m-%d_%H:%M:%S",
    )
    fh = logging.FileHandler("flask.log")
    fh.setLevel(logging.INFO)
    fh.setFormatter(formatter)
    if logger.hasHandlers():
        logger.handlers.clear()
    logger.addHandler(fh)
    logger.propagate = False
    return logger
