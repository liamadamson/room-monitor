"""
Contains a Monitor object, used for reading from sensors and printing to the screen.
"""

from typing import Dict
from room_monitor.io.sensors import sensor
import time

class Monitor:
    """
    Example usage.

        sensors = {
            "sensor_1": FakeSensor(),
            "sensor_2": FakeSensor()
        }
        monitor = Monitor(sensors, 10.0)

        while True:
            monitor.step()
    """
    def __init__(self, sensors: Dict[str, sensor.Sensor], timestep_s: float) -> None:
        """
        :param sensors: Dictionary of sensors to monitor.
        :timestep_s: Time between succesive sensor reads, in seconds.
        """
        self._sensors: Dict[str, sensor.Sensor] = sensors
        self._timestep_s = timestep_s

    def step(self) -> None:
        self.read_sensors()
        self.print_sensor_vals()
        time.sleep(self._timestep_s)

    def read_sensors(self) -> None:
        for name in self._sensors:
            self._sensors[name].read()

    def print_sensor_vals(self) -> None:
        for name in self._sensors:
            print(f"{name}: {self._sensors[name].last_value} {self._sensors[name].unit}")
