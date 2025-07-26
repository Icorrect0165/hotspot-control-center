import subprocess
from typing import Optional, Union, List
import ipaddress

def validate_ip(ip: str) -> bool:
    """Validate an IPv4 address"""
    try:
        ipaddress.IPv4Address(ip)
        return True
    except ipaddress.AddressValueError:
        return False

def run_command(cmd: Union[str, List[str]], 
               timeout: int = 30) -> Optional[str]:
    """Execute a shell command safely"""
    try:
        if isinstance(cmd, str):
            cmd = cmd.split()
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=timeout,
            check=True
        )
        return result.stdout.strip()
    except (subprocess.CalledProcessError, subprocess.TimeoutExpired):
        return None

def sanitize_input(input_str: str) -> str:
    """Sanitize user input for shell commands"""
    return ''.join(
        c for c in input_str 
        if c.isalnum() or c in ('-', '_', '.')
    )