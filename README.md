# Hotspot Control Center (HCC) 🚀

![HCC Logo](webui/static/img/logo.png)

**Enterprise-grade WiFi hotspot management system for Linux with web-based control**

---

## 📚 Table of Contents

- [Key Features](#-key-features)
- [System Requirements](#-system-requirements)
- [Installation Guide](#-installation-guide)
  - [Automated Installation](#automated-installation)
  - [Manual Installation](#manual-installation)
- [Web Interface Usage](#-web-interface-usage)
- [CLI Commands](#cli-commands)
- [Configuration Files](#-configuration-files)
- [Testing Framework](#-testing-framework)
- [Troubleshooting](#-troubleshooting)
- [Security Best Practices](#-security-best-practices)
- [Development](#-development)
- [License](#license)

---

## ✨ Key Features

| Feature               | Description                                              |
|----------------------|----------------------------------------------------------|
| **Unlimited Clients** | Bypass default 8-client limit with hardware-aware scaling |
| **Web Dashboard**     | Modern responsive interface accessible from any device    |
| **Real-time Monitoring** | View connected clients with bandwidth usage           |
| **Bandwidth Control** | Set limits per device or globally                        |
| **Access Control**    | Block/unblock devices by MAC address                     |
| **Hardware Detection**| Automatic NIC capability assessment                      |
| **Multi-Distro Support** | Works on Ubuntu, Debian, RHEL, Arch                  |

---

## 💻 System Requirements

### Hardware
- x86_64 or ARMv7+ processor
- WiFi adapter supporting AP mode (check with `iw list | grep "AP"`)
- Minimum 512MB RAM (1GB recommended for 50+ clients)

### Software
- Linux kernel 4.4+
- Python 3.6+
- Systemd or OpenRC init system

---

## 📥 Installation Guide

### Automated Installation

```bash
# Clone repository
git clone https://github.com/your-repo/hotspot-control-center.git
cd hotspot-control-center

# Run installer (requires root)
sudo ./install.sh
```

### Manual Installation

Install dependencies:

```bash
sudo apt update && sudo apt install -y hostapd dnsmasq python3-pip iw
```

Set up Python environment:

```bash
python3 -m venv /opt/hcc/venv
source /opt/hcc/venv/bin/activate
pip install -r requirements.txt
```

Initialize the database:

```bash
sudo /opt/hcc/bin/hcc --init
```

---

## 🌐 Web Interface Usage

### Accessing the Dashboard

Open your browser and navigate to:

```
http://<your-server-ip>:8080
```

Login credentials will be displayed during installation.

### Interface Overview

| Section    | Functionality                        |
|------------|--------------------------------------|
| Dashboard  | Real-time status and client overview |
| Network    | Configure SSID, password, IP ranges  |
| Clients    | Manage connected devices             |
| Bandwidth  | Set speed limits and QoS             |
| Security   | Configure firewall and access control|

---

## ⚙️ CLI Commands

### Service Management

```bash
# Start/Stop service
sudo systemctl start hcc
sudo systemctl stop hcc

# Check status
sudo hcc status

# View logs
sudo hcc logs
```

### Diagnostics

```bash
# Run all tests
sudo hcc test

# Check WiFi capabilities
sudo hcc wifi-scan

# Benchmark performance
sudo hcc benchmark
```

---

## 🛠 Configuration Files

| File            | Location                  | Purpose                |
|-----------------|--------------------------|------------------------|
| Main Config     | /etc/hcc/config.ini       | Core settings          |
| Hostapd Config  | /etc/hcc/hostapd.conf     | WiFi hotspot parameters|
| DHCP Config     | /etc/hcc/dnsmasq.conf     | IP assignment rules    |
| User Database   | /opt/hcc/var/db/users.db  | Authentication data    |

**Example: `/etc/hcc/config.ini`**

```ini
[network]
interface = wlan0
dhcp_start = 192.168.50.10
dhcp_end = 192.168.50.200
max_clients = 50

[auth]
admin_user = admin
admin_pass = securepassword123
```

---

## 🧪 Testing Framework

### Running Tests

```bash
cd /opt/hcc
python -m pytest tests/ -v
```

### Test Coverage

| Module           | Coverage |
|------------------|----------|
| Authentication   | 95%      |
| Network Config   | 92%      |
| Hardware Detection| 89%     |
| API Endpoints    | 97%      |

---

## 🔧 Troubleshooting

### Hotspot Not Starting

```bash
# Check kernel modules
lsmod | grep cfg80211

# Verify services
sudo systemctl status hostapd
journalctl -u hcc --no-pager -n 50
```

### Web Interface Inaccessible

```bash
# Check firewall
sudo ufw allow 8080/tcp

# Verify process
ps aux | grep hcc
```

### Client Connection Problems

```bash
# Check DHCP leases
cat /var/lib/misc/dnsmasq.leases

# Verify iptables rules
sudo iptables -L -n -v
```

---

## 🔒 Security Best Practices

- Change default credentials immediately after installation.
- Enable HTTPS by adding SSL certificates to webui/app.py.
- Keep system and app updated:

```bash
sudo hcc update
```

- Isolate hotspot network:

```bash
sudo iptables -A FORWARD -i wlan0 -o eth0 -j DROP
```

---

## 🧰 Development

### Contribution Guidelines

1. Fork the repository
2. Create a feature branch:
    ```bash
    git checkout -b feature/AmazingFeature
    ```
3. Commit your changes:
    ```bash
    git commit -m "Add amazing feature"
    ```
4. Push the branch:
    ```bash
    git push origin feature/AmazingFeature
    ```
5. Open a pull request

### Build Process

```bash
# Create deployment package
make package

# Generate documentation
make docs
```

---

## 📄 License

This project is licensed under the MIT License – see the LICENSE file for details.