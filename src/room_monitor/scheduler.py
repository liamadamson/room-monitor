from typing import List, Any
import time
from room_monitor.io import monitor_input


class InputScheduler:

    def __init__(self, inputs: List[monitor_input.MonitorInput[Any]], timestep_s: float) -> None:
        if timestep_s <= 0:
            raise ValueError(f"Timstep must be greater than zero, but {timestep_s} was passed.")

        self._inputs = inputs
        self._timestep_s = timestep_s
        self._last_update_time: float = 0

    def update_inputs(self) -> None:
        for input in self._inputs:
            input.update()

        self._last_update_time = time.time()

    def sleep_until_ready(self) -> None:
        current_time = time.time()
        sleep_time = self._timestep_s - (current_time - self._last_update_time)
        time.sleep(max(sleep_time, 0))
