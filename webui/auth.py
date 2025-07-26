from flask import Blueprint, render_template, request, redirect, url_for, session, flash
from lib.core.auth import authenticate

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form.get('username')
        password = request.form.get('password')
        if authenticate(username, password):
            session['authenticated'] = True
            session['username'] = username
            flash('Login successful', 'success')
            return redirect(url_for('dashboard.index'))
        flash('Invalid credentials', 'danger')
    return render_template('login.html')

@auth_bp.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('auth.login')) 