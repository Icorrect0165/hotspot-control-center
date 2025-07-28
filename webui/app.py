#!/usr/bin/env python3
from flask import Flask, session, redirect, url_for, request, render_template
from lib.core.auth import init_db
from lib.core.network import NetworkManager
import configparser
import logging
import os
import sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import logging
LOG_PATH = os.environ.get("HCC_LOG_PATH", os.path.abspath(os.path.join(os.path.dirname(__file__), "../var/log/hcc-webui.log")))
os.makedirs(os.path.dirname(LOG_PATH), exist_ok=True)

def create_app():
    app = Flask(__name__)
    app.secret_key = os.environ.get('HCC_SECRET_KEY', 'change-this-in-production')
    app.config['API_KEY'] = os.environ.get('HCC_API_KEY', 'dev-api-key')

    # Initialize DB
    init_db()
    net_mgr = NetworkManager()

    # Logging
    logging.basicConfig(
        filename=LOG_PATH,
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

    # Register blueprints
    from webui.first_run import first_run_bp
    from webui.auth import auth_bp
    from webui.dashboard import dashboard_bp

    app.register_blueprint(first_run_bp)
    app.register_blueprint(auth_bp)
    app.register_blueprint(dashboard_bp)

    @app.before_request
    def check_first_run():
        config = configparser.ConfigParser()
        config.read('/etc/hcc/config.ini')
        exempt_endpoints = ['auth.login', 'auth.logout', 'static', 'first_run.setup']
        if (request.endpoint not in exempt_endpoints and
            not config.getboolean('first_run', 'completed', fallback=True)):
            return redirect(url_for('first_run.setup'))

    @app.errorhandler(500)
    def handle_server_error(e):
        app.logger.error(f'Server error: {str(e)}')
        return render_template('500.html'), 500

    @app.route('/network', methods=['GET', 'POST'])
    def network_config():
        # TODO: Implement actual logic or import from blueprint
        return render_template('network.html', page_title="Network Configuration", active_page='network')

    @app.route('/clients')
    def client_management():
        # TODO: Implement actual logic or import from blueprint
        return render_template('clients.html', page_title="Client Management", active_page='clients')

    @app.context_processor
    def inject_api_key():
        return dict(config=app.config)

    return app

if __name__ == '__main__':
    app = create_app()
    app.run(host='0.0.0.0', port=8080, debug=True)