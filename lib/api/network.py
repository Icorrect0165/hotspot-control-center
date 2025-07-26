from flask import jsonify, request
from lib.core.network import NetworkManager
from lib.core.hardware import WiFiAdapter
from functools import wraps

class NetworkAPI:
    def __init__(self, app):
        self.app = app
        self.manager = NetworkManager()
        self.adapter = WiFiAdapter()
        self.register_routes()

    def register_routes(self):
        """Register all network-related API routes"""
        self.app.add_url_rule(
            '/api/network', 
            view_func=self.network_config, 
            methods=['GET', 'POST']
        )
        self.app.add_url_rule(
            '/api/network/capabilities',
            view_func=self.get_capabilities,
            methods=['GET']
        )

    def requires_auth(self, f):
        """Authentication decorator"""
        @wraps(f)
        def decorated(*args, **kwargs):
            if not request.headers.get('X-API-Key') == self.app.config['API_KEY']:
                return jsonify({"error": "Unauthorized"}), 401
            return f(*args, **kwargs)
        return decorated

    def network_config(self):
        """Handle network configuration"""
        if request.method == 'POST':
            try:
                data = request.get_json()
                self.manager.update_config(
                    data.get('ssid'),
                    data.get('password'),
                    data.get('dhcp_start'),
                    data.get('dhcp_end'),
                    int(data.get('max_clients', 32))
                )
                return jsonify({"status": "success"})
            except Exception as e:
                return jsonify({"error": str(e)}), 400
        
        # GET request
        return jsonify({
            "config": self.manager.get_config(),
            "status": self.manager.get_status()
        })

    def get_capabilities(self):
        """Get hardware capabilities"""
        return jsonify(self.adapter.get_capabilities())