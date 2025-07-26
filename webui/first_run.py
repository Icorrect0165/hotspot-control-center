from flask import Blueprint, render_template, redirect, url_for, flash, request
from lib.core.network import NetworkManager
from lib.core.auth import update_admin_password
from webui.forms import FirstRunForm
import configparser

first_run_bp = Blueprint('first_run', __name__)

@first_run_bp.route('/first-run', methods=['GET', 'POST'])
def setup():
    config = configparser.ConfigParser()
    config.read('/etc/hcc/config.ini')
    if config.getboolean('first_run', 'completed', fallback=False):
        return redirect(url_for('dashboard.index'))

    form = FirstRunForm()
    net_manager = NetworkManager()

    if form.validate_on_submit():
        try:
            net_manager.update_config(
                ssid=form.ssid.data or '',
                password=form.password.data or '',
                dhcp_start=form.dhcp_start.data or '',
                dhcp_end=form.dhcp_end.data or '',
                max_clients=form.max_clients.data if form.max_clients.data is not None else 32
            )
            update_admin_password(form.admin_password.data)
            config.set('first_run', 'completed', 'yes')
            with open('/etc/hcc/config.ini', 'w') as f:
                config.write(f)
            flash('Setup complete! Please login with your new credentials', 'success')
            return redirect(url_for('auth.login'))
        except Exception as e:
            flash(f'Configuration failed: {str(e)}', 'danger')

    return render_template('first_run.html', form=form)