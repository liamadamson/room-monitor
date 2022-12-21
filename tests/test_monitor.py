from room_monitor import monitor
from room_monitor.io.sensors import fake_sensor
from room_monitor.io import monitor_input
from unittest.mock import patch
import pytest


@patch("time.sleep")
@pytest.mark.parametrize("timestep_s", [10.0, 30.0])
def test_step(mock_time, timestep_s, capsys):

    monitor_inputs = [
        monitor_input.MonitorInput("input_1", fake_sensor.FakeSensor()),
        monitor_input.MonitorInput("input_1", fake_sensor.FakeSensor()),
        monitor_input.MonitorInput("input_1", fake_sensor.FakeSensor()),
    ]

    monitor_instance = monitor.Monitor(monitor_inputs, timestep_s)
    monitor_instance.step()

    expected = ""

    for input_it in monitor_inputs:
        expected = expected + f"{input_it.name}: 0 {input_it.unit}\n"

    captured = capsys.readouterr()
    assert captured.out == expected

    mock_time.assert_called_with(timestep_s)


@pytest.mark.parametrize("timestep_s", [-15, 0])
def test_bad_timestep(timestep_s):
    sensors = {
        "fake_sensor": fake_sensor.FakeSensor()
    }
    with pytest.raises(ValueError):
        monitor.Monitor(sensors, timestep_s)


def test_empty_sensor_dict():
    with pytest.raises(ValueError):
        monitor.Monitor(dict(), 10.0)