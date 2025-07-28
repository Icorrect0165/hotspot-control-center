import configparser
import subprocess
from typing import Dict
import os
DEFAULT_CONFIG_PATH = os.environ.get("HCC_CONFIG_PATH", os.path.abspath(os.path.join(os.path.dirname(__file__), "../../etc/hcc/config.ini")))

class NetworkManager:
    def __init__(self, config_path=DEFAULT_CONFIG_PATH):
        self.config_path = config_path
        self.config = configparser.ConfigParser()
        self.config.read(self.config_path)

    def validate_config(self) -> bool:
        """Check if minimal config exists"""
        required = ['ssid', 'dhcp_start', 'dhcp_end']
        return all(self.config.get('network', field, fallback=None) for field in required)

    def update_config(self, ssid: str, password: str, 
                    dhcp_start: str, dhcp_end: str,
                    max_clients: int = 32) -> None:
        """Update all network configurations"""
        
        # Validate inputs
        if not all([ssid, dhcp_start, dhcp_end]):
            raise ValueError("Missing required parameters")
        
        # Update hostapd
        self._write_hostapd_config(ssid, password, max_clients)
        
        # Update dnsmasq
        self._write_dnsmasq_config(dhcp_start, dhcp_end)
        
        # Update main config
        self.config['network'] = {
            'interface': 'wlan0',
            'dhcp_start': dhcp_start,
            'dhcp_end': dhcp_end,
            'max_clients': str(max_clients)
        }
        with open(self.config_path, 'w') as f:
            self.config.write(f)
        
        self._restart_services()

    def get_status(self) -> bool:
        """Check if hotspot is active (hostapd running)"""
        import subprocess
        try:
            result = subprocess.run(['systemctl', 'is-active', 'hostapd'], capture_output=True, text=True, check=True)
            return result.stdout.strip() == 'active'
        except Exception:
            return False

    def get_config(self) -> dict:
        """Return current network configuration as a dictionary"""
        return {
            'interface': self.config.get('network', 'interface', fallback='wlan0'),
            'dhcp_start': self.config.get('network', 'dhcp_start', fallback=''),
            'dhcp_end': self.config.get('network', 'dhcp_end', fallback=''),
            'max_clients': self.config.getint('network', 'max_clients', fallback=32)
        }

    def _write_hostapd_config(self, ssid: str, password: str, max_clients: int):
        """Generate secure hostapd config"""
        config = f"""interface=wlan0
driver=nl80211
ssid={ssid}
hw_mode=g
channel=6
wmm_enabled=1
macaddr_acl=0
auth_algs=1
ignore_broadcast_ssid=0
wpa=2
wpa_passphrase={password}
wpa_key_mgmt=WPA-PSK
rsn_pairwise=CCMP
max_num_sta={max_clients}"""
        hostapd_path = os.environ.get("HCC_HOSTAPD_PATH", os.path.abspath(os.path.join(os.path.dirname(__file__), "../../etc/hcc/hostapd.conf")))
        with open(hostapd_path, 'w') as f:
            f.write(config)

    def _write_dnsmasq_config(self, start: str, end: str):
        """Generate dnsmasq config"""
        config = f"""interface=wlan0
dhcp-range={start},{end},12h
address=/hotspot.login/192.168.50.1"""
        dnsmasq_path = os.environ.get("HCC_DNSMASQ_PATH", os.path.abspath(os.path.join(os.path.dirname(__file__), "../../etc/hcc/dnsmasq.conf")))
        with open(dnsmasq_path, 'w') as f:
            f.write(config)

    def _restart_services(self):
        """Restart required services"""
        services = ['hostapd', 'dnsmasq', 'hcc']
        for service in services:
            subprocess.run(['systemctl', 'restart', service], check=True)