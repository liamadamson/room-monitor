"""
Defines an abstract sensor.
"""

from typing import Any
import abc


class Sensor(abc.ABC):

    @abc.abstractmethod
    def read(self) -> Any:
        pass

    @property
    @abc.abstractmethod
    def unit(self) -> str:
        pass
