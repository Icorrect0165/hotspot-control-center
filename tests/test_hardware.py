import pytest
from lib.core.hardware import WiFiAdapter
from unittest.mock import patch, MagicMock

@patch('subprocess.run')
def test_supports_ap_mode(mock_run):
    mock_run.return_value = MagicMock(stdout="Supported interface modes:\n\t\tAP\n")
    adapter = WiFiAdapter()
    assert adapter.supports_ap_mode() is True

@patch('subprocess.run')
def test_get_max_clients(mock_run):
    mock_run.return_value = MagicMock(stdout="Model: MT7612")
    adapter = WiFiAdapter()
    assert adapter.get_max_clients() == 128