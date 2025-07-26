import sqlite3
import bcrypt
import os
from functools import wraps
from flask import redirect, session, flash

def init_db(db_path='/opt/hcc/var/db/users.db'):
    """Initialize the authentication database"""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    
    c.execute('''CREATE TABLE IF NOT EXISTS users
                 (username TEXT PRIMARY KEY, 
                  password TEXT,
                  is_admin BOOLEAN DEFAULT 1)''')
    
    # Create default admin
    default_pass = bcrypt.hashpw(b'admin123', bcrypt.gensalt()).decode()
    c.execute('''INSERT OR IGNORE INTO users 
                 VALUES (?, ?, ?)''', 
              ('admin', default_pass, True))
    conn.commit()
    conn.close()

def authenticate(username, password, db_path='/opt/hcc/var/db/users.db'):
    """Authenticate a user"""
    try:
        conn = sqlite3.connect(db_path)
        c = conn.cursor()
        c.execute('''SELECT password FROM users 
                     WHERE username = ?''', (username,))
        result = c.fetchone()
        conn.close()
        
        if result and bcrypt.checkpw(password.encode(), result[0].encode()):
            return True
    except Exception as e:
        print(f"Authentication error: {e}")
    return False

def update_admin_password(new_password, db_path='/opt/hcc/var/db/users.db'):
    """Update the admin password in the database"""
    hashed = bcrypt.hashpw(new_password.encode(), bcrypt.gensalt()).decode()
    conn = sqlite3.connect(db_path)
    c = conn.cursor()
    c.execute('''UPDATE users SET password = ? WHERE username = ?''', (hashed, 'admin'))
    conn.commit()
    conn.close()

def requires_auth(f):
    """Decorator for protected routes"""
    @wraps(f)
    def decorated(*args, **kwargs):
        if not session.get('authenticated'):
            flash('Please login to access this page', 'warning')
            return redirect('/login')
        return f(*args, **kwargs)
    return decorated