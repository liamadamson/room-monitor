class Monitor:
    
    def __init__(self, timestep_s) -> None:
        if timestep_s < 30:
            raise ValueError(f"Timestep must be at least 30 seconds.")

    def _print_to_screen(self, temp_degc: float, humidity_pc: float) -> None:
        print(f"Temp: {temp_degc} deg C, Humidity: {humidity_pc} %")