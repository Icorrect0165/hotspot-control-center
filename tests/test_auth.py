import pytest
from lib.core.auth import authenticate, init_db
import sqlite3

@pytest.fixture
def test_db(tmp_path):
    db_path = tmp_path / "test_users.db"
    conn = sqlite3.connect(db_path)
    yield db_path
    conn.close()

def test_init_db(test_db):
    init_db(db_path=str(test_db))
    conn = sqlite3.connect(test_db)
    c = conn.cursor()
    c.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='users'")
    assert c.fetchone() is not None

def test_authentication(test_db):
    init_db(db_path=str(test_db))
    assert authenticate("admin", "admin123", db_path=str(test_db)) is True
    assert authenticate("admin", "wrongpass", db_path=str(test_db)) is False