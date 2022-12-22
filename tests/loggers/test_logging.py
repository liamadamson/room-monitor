from typing import Any
from unittest.mock import patch, Mock, call
from room_monitor import logging
from room_monitor.io import monitor_input


class MockInput(monitor_input.MonitorInput):

    def __init__(self, name: str, unit: str, last_val: Any) -> None:
        super().__init__(name, Mock())
        self._name = name
        self._unit = unit
        self._last_val = last_val

    @property
    def name(self):
        return self._name
    
    @property
    def unit(self):
        return self._unit

    @property
    def last_value(self):
        return self._last_val
    

def test_input_logger_log():
    log_handlers = [
        Mock(),
        Mock(),
        Mock()
    ]

    input_logger = logging.InputLogger(log_handlers)

    inputs = [
        MockInput("mock_1", "fake_unit_1", 20.5),
        MockInput("mock_2", "fake_unit_2", 40)
    ]

    input_logger.log(inputs)

    for log_handler in log_handlers:
        log_handler.log.assert_called_with(inputs)


@patch('builtins.print')
def test_print_log_handler(mock_print):
    inputs = [
        MockInput("mock_1", "fake_unit_1", 20.5),
        MockInput("mock_2", "fake_unit_2", 40)
    ]

    print_log_handler = logging.PrintLogHandler()

    print_log_handler.log(inputs)

    calls = [
        call("mock_1: 20.5 fake_unit_1"),
        call("mock_2: 40 fake_unit_2")
    ]

    mock_print.assert_has_calls(calls)
