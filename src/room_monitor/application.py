from room_monitor.io import inputs
import time

class Application:

    def step(self, timestep_s, input_dataclass: inputs.Inputs) -> None:
        temperature = self.get_temperature(input_dataclass)
        humidity = self.get_humidity(input_dataclass)
        self._print_temperature_and_humidity(temperature, humidity)
        time.sleep(timestep_s)
    
    def get_temperature(self, input_dataclass: inputs.Inputs) -> float:
        return input_dataclass.room_temperature.read()

    def get_humidity(self, input_dataclass: inputs.Inputs) -> float:
        return input_dataclass.room_humidity.read()

    def _print_temperature_and_humidity(self, temperature_deg_c: float, humidity_rh: float) -> None:
        print(f"Temperature: {temperature_deg_c} degC, Humidity: {humidity_rh} %RH")