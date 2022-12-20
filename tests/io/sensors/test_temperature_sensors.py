from room_monitor.io.sensors import temperature_sensors
from unittest.mock import Mock
import pytest


@pytest.mark.parametrize("temperature", [18.0, 25.3])
def test_bme280_temp_reader_get_temp(temperature):
    mock_bme280 = Mock()
    mock_bme280.get_temperature.return_value = temperature

    temp_reader = temperature_sensors.BME280TemperatureSensor(mock_bme280)
    assert temp_reader.concrete_read() == temperature


def test_bme280_read_unit():
    mock_bme280 = Mock()
    reader = temperature_sensors.BME280TemperatureSensor(mock_bme280)
    assert reader.unit == "degrees C"