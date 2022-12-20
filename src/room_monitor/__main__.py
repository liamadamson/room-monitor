"""
Main application entry point.
"""

from room_monitor import monitor
from room_monitor.io.sensors import sensor
from room_monitor.io.sensors import temperature_sensors
from room_monitor.io.sensors import humidity_sensors
import bme280 # type: ignore
import smbus2


def get_sensors() -> list[sensor.Sensor]:

    i2c_bus = smbus2.SMBus(1)
    bme280_device = bme280.BME280(i2c_dev=i2c_bus)

    return [
        temperature_sensors.BME280TemperatureSensor(bme280_device),
        humidity_sensors.BME280HumiditySensor(bme280_device)
    ]

sensors = get_sensors()
app = monitor.Monitor(sensors, timestep_s=10.0)
app.run()

