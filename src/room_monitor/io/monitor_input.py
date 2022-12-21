"""
Defines an abstract monitor input.
"""

from typing import Generic, TypeVar, Optional
from room_monitor.io.sensors import sensor


T = TypeVar("T")


class MonitorInput(Generic[T]):

    def __init__(self, name: str, input_sensor: sensor.Sensor[T]) -> None:
        self._name = name
        self._sensor = input_sensor
        self._last_value: Optional[T] = None

    def read(self) -> Optional[T]:
        self.update()
        return self._last_value

    def update(self) -> None:
        self._last_value = self._sensor.read()

    @property
    def name(self) -> str:
        return self._name

    @property
    def last_value(self) -> Optional[T]:
        return self._last_value

    @property
    def unit(self) -> str:
        return self._sensor.unit
