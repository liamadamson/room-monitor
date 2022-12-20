from room_monitor.io import inputs
import time

class Application:

    def __init__(self, inputs_dataclass: inputs.dataclasses) -> None:
        self._inputs_dataclass = inputs_dataclass

    def run(self) -> None:
        while True:
            self.step()

    def step(self, timestep_s) -> None:
        temperature = self.get_temperature()
        humidity = self.get_humidity()
        self._print_temperature_and_humidity(temperature, humidity)
        time.sleep(timestep_s)
    
    def get_temperature(self) -> float:
        return self._inputs_dataclass.room_temperature.read()

    def get_humidity(self) -> float:
        return self._inputs_dataclass.room_humidity.read()

    def _print_temperature_and_humidity(self, temperature_deg_c: float, humidity_rh: float) -> None:
        print(f"Temperature: {temperature_deg_c} degC, Humidity: {humidity_rh} %RH")