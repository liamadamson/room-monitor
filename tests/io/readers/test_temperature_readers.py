from room_monitor.io.readers import temperature_readers
from unittest.mock import patch
import smbus2
import pytest


@pytest.fixture()
def patch_smbus():
    with patch('smbus2.SMBus'):
        yield


@pytest.mark.parametrize("bus_no", [0, 1])
def test_bme_280_reader_uses_i2c_bus_number(patch_smbus, bus_no):
    temp_reader = temperature_readers.BME280TempReader(bus_no)
    smbus2.SMBus.assert_called_with(bus_no)


def test_bme280_reader_uses_i2c_bus_number_1_by_default(patch_smbus):
    temp_reader = temperature_readers.BME280TempReader()
    smbus2.SMBus.assert_called_with(1)


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