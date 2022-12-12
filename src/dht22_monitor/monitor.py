import dataclasses
import Adafruit_DHT
import time

@dataclasses.dataclass
class DHT22Data:
    humidity_percent: float
    temperature_degc: float


class Monitor:
    
    def __init__(self, timestep_s) -> None:
        if timestep_s < 30:
            raise ValueError(f"Timestep must be at least 30 seconds.")

        self.timestep_s = timestep_s
    
    def _print_to_screen(self, temp_degc: float, humidity_pc: float) -> None:
        print(f"Temp: {temp_degc} deg C, Humidity: {humidity_pc} %")


    def _fetch_data(self, gpio_pin: int):
        humidity, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, gpio_pin)
        return DHT22Data(humidity, temp)

    def _step(self):
        dht22_data = self._fetch_data(22)
        self._print_to_screen(dht22_data.temperature_degc, dht22_data.humidity_percent)
        time.sleep(self.timestep_s)