import subprocess
from flask import jsonify, request
from functools import wraps

class ClientAPI:
    def __init__(self, app):
        self.app = app
        self.register_routes()

    def register_routes(self):
        """Register all client-related API routes"""
        self.app.add_url_rule(
            '/api/clients', 
            view_func=self.list_clients, 
            methods=['GET']
        )
        self.app.add_url_rule(
            '/api/clients/block', 
            view_func=self.block_client, 
            methods=['POST']
        )
        self.app.add_url_rule(
            '/api/clients/bandwidth', 
            view_func=self.set_bandwidth, 
            methods=['POST']
        )

    def list_clients(self):
        """List all connected clients"""
        try:
            result = subprocess.run(
                ['arp', '-a'], 
                capture_output=True, 
                text=True
            )
            clients = []
            for line in result.stdout.splitlines():
                if line.strip():
                    parts = line.split()
                    clients.append({
                        "ip": parts[1].strip('()'),
                        "mac": parts[3],
                        "interface": parts[5]
                    })
            return jsonify({"clients": clients})
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    def block_client(self):
        """Block a client by MAC address"""
        data = request.get_json()
        mac = data.get('mac') if data else None
        if not mac:
            return jsonify({"error": "MAC address required"}), 400
        
        try:
            subprocess.run(
                ['iptables', '-A', 'INPUT', '-m', 'mac', '--mac-source', mac, '-j', 'DROP'],
                check=True
            )
            return jsonify({"status": "success"})
        except subprocess.CalledProcessError as e:
            return jsonify({"error": str(e)}), 500

    def set_bandwidth(self):
        """Set bandwidth limit for client"""
        data = request.get_json()
        mac = data.get('mac')
        limit = data.get('limit', '1mbit')
        
        try:
            subprocess.run([
                'tc', 'qdisc', 'add', 'dev', 'wlan0', 'root', 
                'handle', '1:', 'htb', 'default', '12'
            ], check=True)
            subprocess.run([
                'tc', 'class', 'add', 'dev', 'wlan0', 
                'parent', '1:', 'classid', '1:1', 'htb', 
                'rate', limit
            ], check=True)
            return jsonify({"status": "success"})
        except subprocess.CalledProcessError as e:
            return jsonify({"error": str(e)}), 500