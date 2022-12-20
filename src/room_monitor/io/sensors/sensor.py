"""
Defines an abstract sensor.
"""

from typing import Any
import abc


class Sensor(abc.ABC):

    @abc.abstractmethod
    def concrete_read(self) -> Any:
        pass

    @property
    @abc.abstractmethod
    def unit(self) -> str:
        pass
