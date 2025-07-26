#!/bin/bash
set -e

echo "🚀 Hotspot Control Center Installation"
echo "==================================="

# Validate root
[ "$(id -u)" -ne 0 ] && { echo "❌ Run as root"; exit 1; }

# Create structure
echo "📂 Creating directories..."
mkdir -p /opt/hcc/{bin,etc/hcc,lib,webui/static,var/{log,db}}
mkdir -p /etc/systemd/system

# Install dependencies
echo "📦 Installing packages..."
apt update && apt install -y hostapd dnsmasq python3-pip python3-venv iw

# Python environment
echo "🐍 Setting up Python..."
python3 -m venv /opt/hcc/venv
source /opt/hcc/venv/bin/activate
pip install -r requirements.txt

# Generate initial configs
echo "⚙️ Creating default configs..."

cat > /etc/hcc/config.ini <<EOL
[network]
interface = wlan0
dhcp_start = 
dhcp_end = 
max_clients = 

[auth]
admin_user = admin
admin_pass = $(openssl rand -hex 12)

[first_run]
completed = no
EOL

cat > /etc/hcc/hostapd.conf <<EOL
interface=wlan0
driver=nl80211
ssid=HCC-Setup-$(openssl rand -hex 3)
hw_mode=g
channel=6
wmm_enabled=1
ignore_broadcast_ssid=0
EOL

cat > /etc/systemd/system/hcc.service <<EOL
[Unit]
Description=Hotspot Control Center
After=network.target

[Service]
Type=simple
User=root
WorkingDirectory=/opt/hcc/webui
ExecStart=/opt/hcc/venv/bin/python /opt/hcc/webui/app.py
Environment="PYTHONPATH=/opt/hcc"
Restart=always
RestartSec=5

[Install]
WantedBy=multi-user.target
EOL

chmod 640 /etc/hcc/*.conf
chmod 750 /opt/hcc/bin/*

# Enable and start services
echo "🔄 Starting services..."
systemctl daemon-reload
systemctl enable hcc hostapd dnsmasq
systemctl start hcc

echo "✅ Installation complete!"
echo "🌐 Connect to the temporary WiFi: HCC-Setup-*"
echo "🔑 Temporary admin password: $(grep 'admin_pass' /etc/hcc/config.ini | cut -d'=' -f2)"
echo "💻 Configure at http://192.168.50.1:8080/first-run"