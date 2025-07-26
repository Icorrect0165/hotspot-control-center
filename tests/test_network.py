import pytest
from lib.core.network import NetworkManager
import configparser
from unittest.mock import patch, MagicMock

@pytest.fixture
def mock_config(tmp_path):
    config_path = tmp_path / "config.ini"
    config = configparser.ConfigParser()
    config['network'] = {
        'interface': 'wlan0',
        'dhcp_start': '192.168.50.10',
        'dhcp_end': '192.168.50.200',
        'max_clients': '32'
    }
    with open(config_path, 'w') as f:
        config.write(f)
    return config_path

def test_network_manager_init(mock_config):
    nm = NetworkManager(config_path=str(mock_config))
    assert nm.config['network']['interface'] == 'wlan0'

@patch('subprocess.run')
def test_get_status(mock_run, mock_config):
    mock_run.return_value = MagicMock(stdout="active\n")
    nm = NetworkManager(config_path=str(mock_config))
    assert nm.get_status() is True