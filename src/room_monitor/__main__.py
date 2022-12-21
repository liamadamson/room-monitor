"""
Main application entry point.
"""

from typing import List, Any
from room_monitor import monitor
from room_monitor.io import input
from room_monitor.io.sensors import temperature_sensors
from room_monitor.io.sensors import humidity_sensors
import bme280 # type: ignore
import smbus2


def get_inputs() -> List[input.Input[Any]]:
    i2c_bus = smbus2.SMBus(1)
    bme280_device = bme280.BME280(i2c_dev=i2c_bus)

    # Edit here to add or remove sensors.
    return [
        input.Input("Temperature", temperature_sensors.BME280TemperatureSensor(bme280_device)),
        input.Input("Humidity", humidity_sensors.BME280HumiditySensor(bme280_device))
    ]

def main() -> None:
    inputs = get_inputs()
    room_monitor = monitor.Monitor(inputs, timestep_s=10.0)

    while True:
        room_monitor.step()
