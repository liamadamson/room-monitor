"""
Defines an abstract sensor.
"""

from typing import Optional, Generic, TypeVar
import abc


T = TypeVar("T")


class Sensor(abc.ABC, Generic[T]):
    """
    Users of this abstract class should override "concrete_read", not "read".
    """

    def __init__(self) -> None:
        self._last_val: Optional[T] = None

    @abc.abstractmethod
    def concrete_read(self) -> T:
        pass

    @property
    @abc.abstractmethod
    def unit(self) -> str:
        pass

    @property
    def last_value(self) -> Optional[T]:
        return self._last_val

    def read(self) -> T:
        self._last_val = self.concrete_read()
        return self._last_val
