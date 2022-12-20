from room_monitor.io.sensors import sensor
from typing import Any
import abc


class FakeSensor(sensor.Sensor):

    def __init__(self) -> None:
        super().__init__()
        self._val = -1

    def concrete_read(self) -> Any:
        self._val = self._val + 1
        return self._val

    @property
    def unit(self) -> str:
        return "fake"


def test_read_calls_concrete_read():
    fake_sensor = FakeSensor()
    
    for x in range(10):
        assert fake_sensor.read() == x


def test_sensor_initial_last_val_is_none():
    fake_sensor = FakeSensor()
    assert fake_sensor.last_value is None


def test_sensor_last_val_is_updated():
    fake_sensor = FakeSensor()

    for x in range(10):
        fake_sensor.read()
        assert fake_sensor.last_value == x