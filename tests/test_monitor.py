from room_monitor import monitor
from room_monitor.io import inputs  
from room_monitor.io.sensors import fake_sensor
from unittest.mock import patch
import pytest


@patch("time.sleep")
@pytest.mark.parametrize("timestep_s", [10.0, 30.0])
@pytest.mark.parametrize("temp_degc", [20.0, 35.5])
@pytest.mark.parametrize("humid_rh", [40.1, 60.4])
def test_step(mock_time, timestep_s, temp_degc, humid_rh, capsys):
    sensors_list = [
        fake_sensor.FakeSensor(),
        fake_sensor.FakeSensor()
    ]
    
    app = monitor.Monitor(sensors_list, timestep_s)

    def fake_temp_return():
        return temp_degc

    def fake_humid_return():
        return humid_rh

    with patch.object(sensors_list[0], "read", side_effect = fake_temp_return), \
        patch.object(sensors_list[1], "read", side_effect = fake_humid_return):

        app.step(timestep_s)

        captured = capsys.readouterr()
        assert captured.out == f"Temperature: {temp_degc} degC, Humidity: {humid_rh} %RH\n"

        mock_time.assert_called_with(timestep_s)