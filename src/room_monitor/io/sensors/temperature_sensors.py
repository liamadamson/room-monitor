"""
Contains temperature readers.
"""

from room_monitor.io.sensors import sensor
import bme280 # type: ignore


class BME280TemperatureSensor(sensor.Sensor[float]):
    """
    Used to read the temperature, in degrees C, from a BME280 temperature sensor.
    """

    def __init__(self, bme_280: bme280.BME280) -> None:
        super().__init__()
        self._bme_280 = bme_280

    def concrete_read(self) -> float:
        return float(self._bme_280.get_temperature())

    @property
    def unit(self) -> str:
        return "degrees C"
