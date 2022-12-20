"""
Defines the hardware inputs.
"""

import dataclasses
from room_monitor.io.sensors import sensor


@dataclasses.dataclass
class Inputs:
    room_temperature: sensor.Sensor
    room_humidity: sensor.Sensor
