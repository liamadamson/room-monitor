"""
Contains device objects for controlling Raspberry Pi GPIOs.
"""

from types import TracebackType
from typing import Optional, TypeVar
from unittest.mock import Mock
import enum

try:
    import RPi.GPIO as RPi_GPIO
except RuntimeError:
    # Trying to import RPi.GPIO not on a Raspberry Pi causes a RuntimeError.
    # Therefore, we replace RPi.GPIO with a Mock for testing.
    RPi_GPIO = Mock()


class RequiresContextManager(Exception):
    """
    To be raised when the calling object must be created through a context manager, but isn't.
    """


class Direction(enum.Enum):
    """
    Direction of the GPIO pin.
    """
    INPUT = 1
    OUTPUT = 2


class Level(enum.Enum):
    """
    Output level of the GPIO pin.
    """
    HIGH = 1
    LOW = 2


T = TypeVar('T', bound='GPIO')


class GPIO:
    """
    A wrapper object around the standard RPi_GPIO.GPIO module.

    The GPIO object must be used with a context manager to ensure proper cleanup actions.
    """

    def __init__(self) -> None:
        self._pins_setup: set[int] = set()
        self._context_manager_used = False

        # Use the Raspberry Pi GPIO numbering system for GPIO pins, not broadcom.
        RPi_GPIO.setmode(RPi_GPIO.BOARD)

    def __enter__(self: T) -> T:
        self._context_manager_used = True
        return self

    def __exit__(self,
                exc_type: Optional[type[BaseException]],
                exc_value: Optional[BaseException],
                traceback: Optional[TracebackType]) -> None:
        RPi_GPIO.cleanup()

    def setup(self, pin: int, direction: Direction) -> None:
        self._check_context_manager_used()

        if direction == Direction.INPUT:
            RPi_GPIO.setup(pin, RPi_GPIO.IN)
        else:
            RPi_GPIO.setup(pin, RPi_GPIO.OUT)

        self._pins_setup.add(pin)

    def set_output(self, pin: int, value: Level) ->  None:
        self._check_pin_is_setup(pin)

        if value == Level.HIGH:
            RPi_GPIO.output(pin, RPi_GPIO.HIGH)
        else:
            RPi_GPIO.output(pin, RPi_GPIO.LOW)

    def _check_pin_is_setup(self, pin: int) -> None:
        if pin not in self._pins_setup:
            raise RuntimeError

    def _check_context_manager_used(self) -> None:
        if not self._context_manager_used:
            raise RequiresContextManager
