"""
Contains temperature readers.
"""

import smbus2
import bme280 # type: ignore


class BME280TempReader():
    """
    Used to read the temperature, in degrees C, from a BME280 temperature sensor.
    """

    def __init__(self, i2c_bus_no: int = 1) -> None:
        self._bus = smbus2.SMBus(i2c_bus_no)
        self._bme280 = bme280.BME280(i2c_dev=self._bus)

    def read(self) -> float:
        return float(self._bme280.get_temperature())

    @property
    def unit(self) -> str:
        return "degrees C"
