from room_monitor import scheduler
from unittest.mock import Mock, patch
import datetime
import freezegun
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


@patch('time.sleep')
@pytest.mark.parametrize("timestep_s", [30.0, 120.0])
@pytest.mark.parametrize("processing_time_s", [5.0, 20.0])
def test_sleep_until_ready(mock_sleep, timestep_s, processing_time_s):
    inputs = [
        Mock(),
        Mock(),
        Mock()
    ]

    input_scheduler = scheduler.InputScheduler(inputs, timestep_s)

    end_of_update_time = datetime.datetime(2023, 1, 1, 9, 0, 0)
    processing_delta_time = datetime.timedelta(0, processing_time_s)
    end_of_processing_time = end_of_update_time + processing_delta_time

    with freezegun.freeze_time(end_of_update_time):
        input_scheduler.update_inputs()

    with freezegun.freeze_time(end_of_processing_time):
        input_scheduler.sleep_until_ready()

    mock_sleep.assert_called_with(timestep_s - processing_time_s)


@patch('time.sleep')
def test_sleep_until_ready_processing_overrun(mock_sleep):
    inputs = [
        Mock(),
        Mock(),
        Mock()
    ]

    input_scheduler = scheduler.InputScheduler(inputs, 10.0)

    end_of_update_time = datetime.datetime(2023, 1, 1, 9, 0, 0)
    processing_delta_time = datetime.timedelta(0, 15.0)
    end_of_processing_time = end_of_update_time + processing_delta_time

    with freezegun.freeze_time(end_of_update_time):
        input_scheduler.update_inputs()

    with freezegun.freeze_time(end_of_processing_time):
        input_scheduler.sleep_until_ready()

    mock_sleep.assert_called_with(0)