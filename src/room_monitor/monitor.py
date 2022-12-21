"""
Contains a Monitor object, which is used for reading from sensors and printing values to the screen.
"""

from typing import List, Any
from room_monitor.io import input
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
    def __init__(self, inputs: List[input.Input[Any]], timestep_s: float) -> None:
        """
        :param sensors: Dictionary of sensors to monitor.
        :timestep_s: Time between succesive sensor reads, in seconds.
        """
        if timestep_s <= 0:
            raise ValueError(f"timestep_s must be greater than zero, but {timestep_s} was passed.")

        if len(inputs) < 1:
            raise ValueError("There must be at least one sensor to read from.")

        self._inputs = inputs
        self._timestep_s = timestep_s

    def step(self) -> None:
        self._update_inputs()
        self._print_inputs()
        time.sleep(self._timestep_s)

    def _update_inputs(self) -> None:
        for input_it in self._inputs:
            input_it.update()

    def _print_inputs(self) -> None:
        for input_it in self._inputs:
            print(f"{input_it.name}: {input_it.last_value} {input_it.unit}")
