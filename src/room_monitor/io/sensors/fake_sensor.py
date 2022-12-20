from room_monitor.io.sensors import sensor

class FakeSensor(sensor.Sensor):
    
    def __init__(self) -> None:
        self._val = -1

    def concrete_read(self) -> int:
        self._val = self._val + 1
        return self._val

    @property
    def unit(self) -> str:
        return "fake unit"