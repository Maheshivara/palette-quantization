from abc import ABC, abstractmethod
from enum import Enum


class LoggerLevel(Enum):
    MUTE = 0
    ERROR = 1
    WARNING = 2
    INFO = 3
    DEBUG = 4


class Logger(ABC):
    def __init__(self, level: LoggerLevel) -> None:
        super().__init__()
        self._level = level

    @abstractmethod
    def error(self, msg: str):
        pass

    @abstractmethod
    def warning(self, msg: str):
        pass

    @abstractmethod
    def info(self, msg: str):
        pass

    @abstractmethod
    def debug(self, msg: str):
        pass
