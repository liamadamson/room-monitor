"""
Contains the main Application object.
"""

from typing import Dict
from room_monitor.io.sensors import sensor
import time

class Monitor:
    """
    Main application object.
    """

    def __init__(self, sensor_dict: Dict[str, sensor.Sensor], timestep_s: float) -> None:
        self._sensors: Dict[str, sensor.Sensor] = sensor_dict
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
