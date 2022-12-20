from dataclasses import dataclass
from room_monitor.io import inputs
from room_monitor.io.sensors import fake_sensor
import dataclasses
import pytest


def test_inputs_dataclass_names() -> None:
    expected_field_names = [
        "room_temperature",
        "room_humidity"
    ]

    actual_field_names =  [field.name for field in dataclasses.fields(inputs.Inputs)]

    assert expected_field_names == actual_field_names


@pytest.mark.skip
def test_print_inputs(capsys) -> None:
    inputs_dataclass = inputs.Inputs(
        fake_sensor.FakeSensor(),
        fake_sensor.FakeSensor()
    )

    inputs.print_inputs(inputs_dataclass)

    captured = capsys.readouterr()

    expected = ""