
from mock import patch
from tableprinter import utils

@patch('tableprinter.utils.subprocess')
def test_get_terminal_width_nominal(subp_mock):
    subp_mock.check_output.return_value = '100\n'

    assert utils.get_terminal_width() == 100
    subp_mock.check_output.assert_called_once_with(['tput', 'cols'])

@patch('tableprinter.utils.subprocess')
def test_get_terminal_width_error(subp_mock):
    subp_mock.check_output.side_effect = RuntimeError()

    assert utils.get_terminal_width(fallback_width=99) == 99
    subp_mock.check_output.assert_called_once_with(['tput', 'cols'])

def test_pad_ellipse():
    assert utils.pad_ellipse('hello', 10) == "hello     "
    assert utils.pad_ellipse('hello', 10, align='>') == "     hello"
    assert utils.pad_ellipse('hello', 5) == "hello"

    assert utils.pad_ellipse('hello world', 5) == "hel.."
