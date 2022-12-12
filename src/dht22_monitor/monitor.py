class Monitor:
    
    def __init__(self, timestep_s) -> None:
        if timestep_s < 30:
            raise ValueError(f"Timestep must be at least 30 seconds.")