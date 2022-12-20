"""
Defines an abstract sensor.
"""

from typing import Any
import abc


class Sensor(abc.ABC):

    def __init__(self) -> None:
        self._last_val = None

    @abc.abstractmethod
    def concrete_read(self) -> Any:
        pass

    @property
    @abc.abstractmethod
    def unit(self) -> str:
        pass

    @property
    def last_value(self) -> None:
        return self._last_val

    def read(self) -> None:
        self._last_val = self.concrete_read()
        return self._last_val