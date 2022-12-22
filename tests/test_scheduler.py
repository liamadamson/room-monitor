from room_monitor import scheduler
from unittest.mock import Mock
import pytest


@pytest.mark.parametrize("timestep_s", [-10, -1, 0])
def test_bad_timestep(timestep_s):
    with pytest.raises(ValueError):
        scheduler.InputScheduler(Mock(), timestep_s)


def test_update_inputs():
    inputs = [
        Mock(),
        Mock(),
        Mock()
    ]

    input_scheduler = scheduler.InputScheduler(inputs, 10.0)

    input_scheduler.update_inputs()

    for input in inputs:
        input.update.assert_called()
