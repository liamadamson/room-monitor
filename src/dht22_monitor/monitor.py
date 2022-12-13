"""Used to continuously monitor and print data from a DHT22 sensor."""

import dataclasses
import time
import Adafruit_DHT # type: ignore


@dataclasses.dataclass
class DHT22Data:
    """
    A dataclass containing humidity and temperature readings from the DHT22 sensor.
    """
    humidity_percent: float
    temperature_degc: float


class Monitor:
    """
    Used to monitor and print humidity and temperature data from a DHT22 sensor.
    """

    def __init__(self, timestep_s: float, gpio_pin: int) -> None:
        if timestep_s < 30:
            raise ValueError(f"Timestep must be at least 30 seconds.")

        self._timestep_s = timestep_s
        self._gpio_pin = gpio_pin

    def run(self) -> None:
        """
        Runs the monitor.
        """
        while True:
            self._step()

    def _print_to_screen(self, temp_degc: float, humidity_pc: float) -> None:
        print(f"Temperature: {temp_degc} deg C, Humidity: {humidity_pc} %")

    def _fetch_data(self, gpio_pin: int) -> DHT22Data:
        humidity, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, gpio_pin)
        return DHT22Data(humidity, temp)

    def _step(self) -> None:
        dht22_data = self._fetch_data(self._gpio_pin)
        self._print_to_screen(dht22_data.temperature_degc, dht22_data.humidity_percent)
        time.sleep(self._timestep_s)
