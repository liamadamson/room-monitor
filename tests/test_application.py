from room_monitor import application
from room_monitor.io import inputs  
from room_monitor.io.sensors import fake_sensor
from unittest.mock import patch
import pytest


@patch("time.sleep")
@pytest.mark.parametrize("timestep_s", [10.0, 30.0])
@pytest.mark.parametrize("temp_degc", [20.0, 35.5])
@pytest.mark.parametrize("humid_rh", [40.1, 60.4])
def test_step(mock_time, timestep_s, temp_degc, humid_rh, capsys):
    app = application.Application()

    inputs_dataclass = inputs.Inputs(
        fake_sensor.FakeSensor(),
        fake_sensor.FakeSensor()
    )

    def fake_temp_return():
        return temp_degc

    def fake_humid_return():
        return humid_rh

    with patch.object(inputs_dataclass.room_temperature, "read", side_effect = fake_temp_return), \
        patch.object(inputs_dataclass.room_humidity, "read", side_effect = fake_humid_return):

        app.step(timestep_s, inputs_dataclass)

        captured = capsys.readouterr()
        assert captured.out == f"Temperature: {temp_degc} degC, Humidity: {humid_rh} %RH\n"

        mock_time.assert_called_with(timestep_s)