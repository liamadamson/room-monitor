from room_monitor import application
from room_monitor.io import inputs  
import pytest


def test_print_sensor_data(capsys):

    temperature = 30.0
    humidity = 45.5

    app = application.Application()
    app._print_temperature_and_humidity(temperature, humidity)
    
    captured = capsys.readouterr()

    assert captured.out == f"Temperature: {temperature} degC, Humidity: {humidity} %RH\n"
