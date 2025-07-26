import pytest
from lib.core.auth import init_db
import sqlite3
import tempfile

@pytest.fixture(scope="session", autouse=True)
def setup_tests():
    """Global test setup"""
    # Create a temporary directory for test databases
    with tempfile.TemporaryDirectory() as tmp_dir:
        yield