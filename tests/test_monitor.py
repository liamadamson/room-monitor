import pytest
from dht22_monitor import monitor

@pytest.mark.parametrize("timestep_s", [-5, 0, 29.9])
def test_bad_time_step(timestep_s):
    with pytest.raises(ValueError):
        monitor.Monitor(timestep_s)