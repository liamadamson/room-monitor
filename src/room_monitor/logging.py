"""
For logging monitor inputs.
"""

import abc
import datetime
from typing import Sequence, Any
from room_monitor.io import monitor_input


class LogHandler(abc.ABC):

    @abc.abstractmethod
    def log(self, inputs: Sequence[monitor_input.MonitorInput[Any]]) -> None:
        pass


class InputLogger:

    def __init__(self, log_handlers: Sequence[LogHandler]) -> None:
        self._log_handlers = log_handlers

    def log(self, inputs: Sequence[monitor_input.MonitorInput[Any]]) -> None:
        for log_handler in self._log_handlers:
            log_handler.log(inputs)


class PrintLogHandler(LogHandler):

    def log(self, inputs: Sequence[monitor_input.MonitorInput[Any]]) -> None:
        self._print_header()

        for input_it in inputs:
            print(f"{input_it.name}: {input_it.last_value} {input_it.unit}")

    def _print_header(self) -> None:
        print(f"========== {datetime.datetime.now()} ==========")
