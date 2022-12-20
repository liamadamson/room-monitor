"""
Main application entry point.
"""

from room_monitor import application
from room_monitor.io import inputs
from room_monitor.io.sensors import temperature_sensors
from room_monitor.io.sensors import humidity_sensors
import bme280
import smbus2


def get_inputs_dataclass() -> inputs.Inputs:

    i2c_bus = smbus2.SMBus(1)
    bme280_device = bme280.BME280(i2c_dev=i2c_bus)

    return inputs.Inputs(
        room_temperature=temperature_sensors.BME280TemperatureSensor(bme280_device),
        room_humidity=humidity_sensors.BME280HumiditySensor(bme280_device)
    )

inputs_dataclass = get_inputs_dataclass()
app = application.Application(inputs_dataclass)
app.run()

