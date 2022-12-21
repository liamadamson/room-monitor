"""
Main application entry point.
"""

from typing import Dict
from room_monitor import monitor
from room_monitor.io.sensors import sensor
from room_monitor.io.sensors import temperature_sensors
from room_monitor.io.sensors import humidity_sensors
import bme280 # type: ignore
import smbus2


def get_sensors() -> Dict[str, sensor.Sensor[float]]:
    i2c_bus = smbus2.SMBus(1)
    bme280_device = bme280.BME280(i2c_dev=i2c_bus)

    # Edit here to add or remove sensors.
    return {
        "Temperature": temperature_sensors.BME280TemperatureSensor(bme280_device),
        "Humidity": humidity_sensors.BME280HumiditySensor(bme280_device)
    }

def main() -> None:
    sensors = get_sensors()
    room_monitor = monitor.Monitor(sensors, timestep_s=10.0)

    while True:
        room_monitor.step()
