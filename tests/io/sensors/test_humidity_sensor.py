from room_monitor.io.sensors import humidity_sensors
from unittest.mock import Mock
import pytest


@pytest.mark.parametrize("humidity", [40.0, 57.8])
def test_bme280_humidity_sensor_get_humidity(humidity):
    mock_bme280 = Mock()
    mock_bme280.get_humidity.return_value = humidity

    sensor = humidity_sensors.BME280HumiditySensor(mock_bme280)
    assert sensor.concrete_read() == humidity


def test_bme280_humidity_sensor_unit():
    mock_bme280 = Mock()
    sensor = humidity_sensors.BME280HumiditySensor(mock_bme280)
    assert sensor.unit == "% RH"