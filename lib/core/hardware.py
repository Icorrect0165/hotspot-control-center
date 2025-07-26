import subprocess
import re
from typing import Dict, Optional

class WiFiAdapter:
    def __init__(self, interface: str = 'wlan0'):
        self.interface = interface

    def get_capabilities(self) -> Dict:
        """Get all hardware capabilities"""
        return {
            'interface': self.interface,
            'supports_ap': self.supports_ap_mode(),
            'max_clients': self.get_max_clients(),
            'signal_strength': self.get_signal_strength()
        }

    def supports_ap_mode(self) -> bool:
        """Check if AP mode is supported"""
        try:
            result = subprocess.run(
                ['iw', 'list'],
                capture_output=True,
                text=True,
                check=True
            )
            return "AP" in result.stdout
        except subprocess.CalledProcessError:
            return False

    def get_max_clients(self) -> int:
        """Get maximum supported clients"""
        chipset = self._get_chipset()
        limits = {
            'AX200': 200,    # Intel WiFi 6
            'MT7612': 128,   # MediaTek
            'RT2800': 64,    # Ralink
            'default': 32
        }
        return next((v for k, v in limits.items() if k in chipset), limits['default'])

    def get_signal_strength(self) -> Optional[int]:
        """Get signal strength in dBm"""
        try:
            result = subprocess.run(
                ['iwconfig', self.interface],
                capture_output=True,
                text=True,
                check=True
            )
            match = re.search(r'Signal level=(-?\d+) dBm', result.stdout)
            return int(match.group(1)) if match else None
        except subprocess.CalledProcessError:
            return None

    def _get_chipset(self) -> str:
        """Identify WiFi chipset"""
        try:
            result = subprocess.run(
                ['lspci', '-nnk'],
                capture_output=True,
                text=True,
                check=True
            )
            return result.stdout
        except subprocess.CalledProcessError:
            return "Unknown"