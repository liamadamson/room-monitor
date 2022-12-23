"""
Main application entry point.
"""

from typing import List, Any
from room_monitor.io import monitor_input
from room_monitor.io.sensors import temperature_sensors
from room_monitor.io.sensors import humidity_sensors
from room_monitor import logging
from room_monitor import scheduler
import bme280 # type: ignore
import smbus2


def get_inputs() -> List[monitor_input.MonitorInput[Any]]:
    i2c_bus = smbus2.SMBus(1)
    bme280_device = bme280.BME280(i2c_dev=i2c_bus)

    # Edit here to add or remove sensors.
    return [
        monitor_input.MonitorInput(
            "Temperature",
            temperature_sensors.BME280TemperatureSensor(bme280_device)
            ),
        monitor_input.MonitorInput(
            "Humidity",
            humidity_sensors.BME280HumiditySensor(bme280_device)
            )
    ]

def get_input_logger() -> logging.InputLogger:
    log_handlers = [
        logging.PrintLogHandler()
    ]
    return logging.InputLogger(log_handlers)

def main() -> None:
    inputs = get_inputs()
    logger = get_input_logger()
    input_scheduler = scheduler.InputScheduler(inputs, 10.0)

    while True:
        input_scheduler.update_inputs()
        logger.log(inputs)
        input_scheduler.sleep_until_ready()
