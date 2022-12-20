"""
Defines an abstract sensor.
"""

from typing import Optional
import abc


class Sensor(abc.ABC):
    """
    Users of this abstract class should override "concrete_read", not "read".
    """

    def __init__(self) -> None:
        self._last_val: Optional[float] = None

    @abc.abstractmethod
    def concrete_read(self) -> float:
        pass

    @property
    @abc.abstractmethod
    def unit(self) -> str:
        pass

    @property
    def last_value(self) -> Optional[float]:
        return self._last_val

    def read(self) -> float:
        self._last_val = self.concrete_read()
        return self._last_val
