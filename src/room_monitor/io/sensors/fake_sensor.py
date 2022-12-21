"""
Contains a fake sensor used for testing.
"""

from room_monitor.io.sensors import sensor

class FakeSensor(sensor.Sensor[int]):
    """
    A fake sensor used for testing. A call to read will return a counter, which is incremented
    by 1.
    """

    def __init__(self) -> None:
        super().__init__()
        self._val = -1

    def concrete_read(self) -> int:
        self._val = self._val + 1
        return self._val

    @property
    def unit(self) -> str:
        return "fake unit"
