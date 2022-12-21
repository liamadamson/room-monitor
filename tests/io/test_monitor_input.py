from room_monitor.io import monitor_input
from room_monitor.io.sensors import fake_sensor
from unittest.mock import Mock
import pytest


@pytest.mark.parametrize("name", ["input1", "input2"])
def test_input_name(name):
    mock_sensor = Mock()
    input_instance = monitor_input.MonitorInput(name, mock_sensor)
    assert input_instance.name == name


def test_get_unit():
    input_instance = monitor_input.MonitorInput("fake_input", fake_sensor.FakeSensor())

    input_instance.unit == "fake unit"


def test_update_calls_sensor_read():
    mock_sensor = Mock()
    input_instance = monitor_input.MonitorInput("fake_input", mock_sensor)
    input_instance.update()
    mock_sensor.read.assert_called()

def test_read_returns_sensor_read():
    mock_sensor = Mock()
    mock_sensor.read.return_value = 5.0
    input_instance = monitor_input.MonitorInput("fake_input", mock_sensor)
    assert input_instance.read() == 5.0

def test_initial_last_value_is_none():
    mock_sensor = Mock()
    fake_input = monitor_input.MonitorInput("fake_input", mock_sensor)
    assert fake_input.last_value is None


def test_update_updates_last_val():
    mock_sensor = Mock()
    mock_sensor.read.return_value = 5.0
    input_instance = monitor_input.MonitorInput("fake_input", mock_sensor)
    input_instance.update()
    assert input_instance.last_value == 5.0

def test_read_updates_last_val():
    mock_sensor = Mock()
    mock_sensor.read.return_value = 5.0
    input_instance = monitor_input.MonitorInput("fake_input", mock_sensor)
    input_instance.read()
    assert input_instance.last_value == 5.0
