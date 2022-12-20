import time

class Application:  
    def print_data(self, temperature_deg_c: float, humidity_rh: float) -> None:
        print(f"Temperature: {temperature_deg_c} degC, Humidity: {humidity_rh} % RH")

    def step(self, step_time_s: float, temperature_deg_c: float, humidity_rh: float) -> None:
        self.print_data(temperature_deg_c, humidity_rh)
        time.sleep(step_time_s)