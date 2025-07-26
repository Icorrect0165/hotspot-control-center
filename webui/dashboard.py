from flask import Blueprint, render_template, session
from lib.core.network import NetworkManager

dashboard_bp = Blueprint('dashboard', __name__)

@dashboard_bp.route('/')
def index():
    net_mgr = NetworkManager()
    status = net_mgr.get_status()
    return render_template('dashboard.html', status=status, page_title="Dashboard", active_page='dashboard') 