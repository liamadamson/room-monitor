import pytest
from unittest.mock import patch
from dht22_monitor import monitor
import Adafruit_DHT


@pytest.fixture(name="monitor_instance")
def fixture_monitor_instance():
    return monitor.Monitor(30.0)


@pytest.mark.parametrize("timestep_s", [-5, 0, 29.9])
def test_bad_time_step(timestep_s):
    with pytest.raises(ValueError):
        monitor.Monitor(timestep_s)


def test_print_to_screen(monitor_instance, capsys):
    temp_degc = 22.0
    humidity_pc = 50.0

    monitor_instance._print_to_screen(temp_degc, humidity_pc)

    desired_output = f"Temp: {temp_degc} deg C, Humidity: {humidity_pc} %\n"

    captured = capsys.readouterr()
    assert captured.out == desired_output


@pytest.mark.parametrize("gpio_pin", [3, 6, 10])
def test_fetch_data(monitor_instance, gpio_pin):
    humidity_pc = 60.0
    temperature_degc = 25.0
    
    expected = monitor.DHT22Data(humidity_pc, temperature_degc)

    def fake_return(*args):
        return (humidity_pc, temperature_degc)

    with patch("Adafruit_DHT.read_retry", side_effect=fake_return):
        data = monitor_instance._fetch_data(gpio_pin)

        Adafruit_DHT.read_retry.assert_called_with(Adafruit_DHT.DHT22, gpio_pin)

    assert data == expected