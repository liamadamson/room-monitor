"""
Contains the main Application object.
"""

from room_monitor.io.sensors import sensor
import time

class Monitor:
    """
    Main application object.
    """

    def __init__(self, sensors: list[sensor.Sensor], timestep_s: float) -> None:
        self._sensors = sensors
        self._timestep_s = timestep_s

    def run(self) -> None:
        while True:
            self.step(self._timestep_s)

    def step(self, timestep_s: float) -> None:
        temperature = self.get_temperature()
        humidity = self.get_humidity()
        self._print_temperature_and_humidity(temperature, humidity)
        time.sleep(timestep_s)

    def get_temperature(self) -> float:
        return self._sensors[0].read()

    def get_humidity(self) -> float:
        return self._sensors[1].read()

    def _print_temperature_and_humidity(self, temperature_deg_c: float, humidity_rh: float) -> None:
        print(f"Temperature: {temperature_deg_c} degC, Humidity: {humidity_rh} %RH")
