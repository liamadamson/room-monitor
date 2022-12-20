from unittest.mock import Mock

try:
    import RPi.GPIO as GPIO
except:
    GPIO = Mock()

class LED:

    def __init__(self, gpio_pin: int) -> None:
        self._gpio_pin = gpio_pin

    def turn_on(self):
        GPIO.output(self._gpio_pin, True)

    def turn_off(self):
        GPIO.output(self._gpio_pin, False)

    def setup() -> None:
        GPIO.setup()
