from room_monitor import application
from unittest.mock import patch
import pytest


@pytest.mark.parametrize("temperature", [20.0, 40.5])
@pytest.mark.parametrize("humidity", [40.0, 60.5])
def test_print_data(temperature, humidity, capsys):
    app = application.Application()
    app.print_data(temperature, humidity)
    
    captured = capsys.readouterr()

    assert captured.out == f"Temperature: {temperature} degC, Humidity: {humidity} % RH\n"


@patch("time.sleep")
@patch.object(application.Application, 'print_data')
@pytest.mark.parametrize("step_time_s", [1.0, 30.0])
def test_step(mock_print_data, mock_sleep, step_time_s):
    temperature = 35.0
    humidity = 40.0

    app = application.Application()

    app.step(step_time_s, temperature, humidity)
    mock_print_data.assert_called_with(temperature, humidity)
    mock_sleep.assert_called_with(step_time_s)