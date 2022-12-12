import dataclasses
import Adafruit_DHT

@dataclasses.dataclass
class DHT22Data:
    humidity_percent: float
    temperature_degc: float


class Monitor:
    
    def __init__(self, timestep_s) -> None:
        if timestep_s < 30:
            raise ValueError(f"Timestep must be at least 30 seconds.")

    
    def _print_to_screen(self, temp_degc: float, humidity_pc: float) -> None:
        print(f"Temp: {temp_degc} deg C, Humidity: {humidity_pc} %")


    def _fetch_data(self, gpio_pin: int):
        humidity, temp = Adafruit_DHT.read_retry(Adafruit_DHT.DHT22, gpio_pin)
        return DHT22Data(humidity, temp)