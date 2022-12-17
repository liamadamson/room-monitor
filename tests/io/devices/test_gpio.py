import pytest
from room_monitor.io.devices import gpio


def test_exit_calls_cleanup():
    with gpio.GPIO():
        pass
    gpio.RPi_GPIO.cleanup.assert_called()


def test_enter_sets_pin_numbering():
    with gpio.GPIO():
        gpio.RPi_GPIO.setmode.assert_called_with(gpio.RPi_GPIO.BOARD)


@pytest.mark.parametrize("channel", [7, 17])
@pytest.mark.parametrize("direction", [gpio.Direction.INPUT, gpio.Direction.OUTPUT])
def test_setup_channel(channel, direction):
    with gpio.GPIO() as gpio_device:
        gpio_device.setup(channel, direction)

        if direction == gpio.Direction.INPUT:
            direction_RPi = gpio.RPi_GPIO.IN
        else:
            direction_RPi = gpio.RPi_GPIO.OUT

        gpio.RPi_GPIO.setup.assert_called_with(channel, direction_RPi)


@pytest.mark.parametrize("channel", [7, 17])
@pytest.mark.parametrize("pin_value", [gpio.Level.HIGH, gpio.Level.HIGH])
def test_set_output(channel, pin_value):
    with gpio.GPIO() as gpio_device:
        gpio_device.setup(channel, gpio.Direction.OUTPUT)
        gpio_device.set_output(channel, pin_value)

        if pin_value == gpio.Level.HIGH:
            output_RPi = gpio.RPi_GPIO.HIGH
        else:
            output_RPi = gpio.RPi_GPIO.LOW

        gpio.RPi_GPIO.output.assert_called_with(channel, output_RPi)


@pytest.mark.parametrize("pin", [7, 17])
def test_set_output_requires_pin_setup(pin):
    with gpio.GPIO() as gpio_device:
        with pytest.raises(RuntimeError):
            gpio_device.set_output(pin, gpio.Level.HIGH)
        

def test_setup_channel_requires_context_manager():
    gpio_device = gpio.GPIO()
    with pytest.raises(gpio.RequiresContextManager):
        gpio_device.setup(7, gpio.Direction.OUTPUT)
