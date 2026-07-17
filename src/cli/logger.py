from core.domain.logger import Logger, LoggerLevel
from halo import Halo


class CLILogger(Logger):
    def __init__(self, level: LoggerLevel = LoggerLevel.INFO) -> None:
        super().__init__(level)
        self._spinner = Halo()
        self._spinner.start()

    def _reset(self):
        self._spinner = Halo()
        self._spinner.start()

    def error(self, msg: str):
        if self._level.value < LoggerLevel.ERROR.value:
            return
        self._spinner.fail(msg)
        exit(1)

    def warning(self, msg: str):
        if self._level.value < LoggerLevel.WARNING.value:
            return

        self._spinner.warn(msg)
        self._reset()

    def info(self, msg: str):
        if self._level.value < LoggerLevel.INFO.value:
            return

        self._spinner.info(msg)
        self._reset()

    def debug(self, msg: str):
        if self._level.value < LoggerLevel.DEBUG.value:
            return

        self._spinner.info(f"DEBUG: {msg}")
        self._reset()

    def complete(self,msg:str):
        self._spinner.succeed(msg)
