from room_monitor.io.outputs import led
from unittest.mock import patch
import pytest


@pytest.mark.skip
@pytest.mark.parametrize("gpio_pin", [7, 17])
def test_led_turn_on(gpio_pin):
    led_writer = led.LED(gpio_pin)
    led_writer.turn_on()
    led.GPIO.output.assert_called_with(gpio_pin, True)


@pytest.mark.skip
@pytest.mark.parametrize("gpio_pin", [7, 17])
def test_led_turn_off(gpio_pin):
    led_writer = led.LED(gpio_pin)
    led_writer.turn_off()
    led.GPIO.output.assert_called_with(gpio_pin, False)


@pytest.mark.skip
@pytest.mark.parametrize("gpio_pin", [7, 17])
def test_led_init_calls_GPIO_setup(gpio_pin):
    led_writer = led.LED(gpio_pin)
    led.GPIO.setup.assert_called_with(gpio_pin, led.GPIO.out)