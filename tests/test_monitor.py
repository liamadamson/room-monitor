from room_monitor import monitor
from room_monitor.io.sensors import fake_sensor
from unittest.mock import patch
import pytest


@patch("time.sleep")
@pytest.mark.parametrize("timestep_s", [10.0, 30.0])
def test_step(mock_time, timestep_s, capsys):

    fake_sensor_instance = fake_sensor.FakeSensor()

    with patch.object(fake_sensor_instance, "read"):

        sensors = {
            "sensor1": fake_sensor.FakeSensor(),
            "sensor2": fake_sensor.FakeSensor(),
            "sensor3": fake_sensor.FakeSensor()
        }

        app = monitor.Monitor(sensors, timestep_s)
        app.step()

        expected = ""

        for sensor in sensors:
            expected = expected + f"{sensor}: 0 fake unit\n"

        captured = capsys.readouterr()
        assert captured.out == expected

        mock_time.assert_called_with(timestep_s)