"""
Contains sensors for reading the humidity.
"""

from room_monitor.io.sensors import sensor
import bme280 # type: ignore


class BME280HumiditySensor(sensor.Sensor):
    """
    Used to read the humidity, in percentage relative humidity, from a BME280.
    """

    def __init__(self, bme_280: bme280.BME280) -> None:
        self._bme_280 = bme_280

    def concrete_read(self) -> float:
        return float(self._bme_280.get_humidity())

    @property
    def unit(self) -> str:
        return "% RH"
