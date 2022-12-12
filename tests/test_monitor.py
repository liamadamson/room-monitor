import pytest
from dht22_monitor import monitor


@pytest.fixture(name="monitor_instance")
def fixture_monitor_instance():
    return monitor.Monitor(30.0)


@pytest.mark.parametrize("timestep_s", [-5, 0, 29.9])
def test_bad_time_step(timestep_s):
    with pytest.raises(ValueError):
        monitor.Monitor(timestep_s)


def test_print_to_screen(monitor_instance, capsys):
    temp_degc = 22.0
    humidity_pc = 50.0

    monitor_instance._print_to_screen(temp_degc, humidity_pc)

    desired_output = f"Temp: {temp_degc} deg C, Humidity: {humidity_pc} %\n"

    captured = capsys.readouterr()
    assert captured.out == desired_output