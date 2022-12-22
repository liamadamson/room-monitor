from typing import List, Any
from room_monitor.io import monitor_input


class InputScheduler:
    
    def __init__(self, inputs: List[monitor_input.MonitorInput[Any]], timestep_s: float) -> None:
        if timestep_s <= 0:
            raise ValueError(f"Timstep must be greater than zero, but {timestep_s} was passed.")

        self._inputs = inputs

    def update_inputs(self) -> None:
        for input in self._inputs:
            input.update()

