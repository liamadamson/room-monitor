from room_monitor.io.readers import temperature_readers
from unittest.mock import patch
import pytest


@pytest.fixture()
def patch_smbus():
    with patch('smbus2.SMBus'):
        yield


@pytest.mark.parametrize("temperature", [18.0, 25.3])
def test_bme280_temp_reader_get_temp(temperature, patch_smbus):
    def fake_get_temperature(*args):
        return temperature

    with patch('bme280.BME280.get_temperature', side_effect=fake_get_temperature):
        temp_reader = temperature_readers.BME280TempReader()
        assert temp_reader.read() == temperature


def test_bme280_read_unit(patch_smbus):
    reader = temperature_readers.BME280TempReader()
    assert reader.unit == "degrees C"