"""Test setup: point the app at a fresh, temporary SQLite database before it is imported."""
import os
import sys
import tempfile
from pathlib import Path

import pytest

_DB_DIR = tempfile.mkdtemp(prefix="fastfastapi-tests-")
os.environ["DATABASE_URL"] = f"sqlite:///{Path(_DB_DIR) / 'test_users.db'}"
sys.path.insert(0, str(Path(__file__).resolve().parents[1]))

from fastapi.testclient import TestClient  # noqa: E402

from database import Base, engine  # noqa: E402
from myapi import app  # noqa: E402


@pytest.fixture()
def client():
    """A test client with empty tables for every test."""
    Base.metadata.drop_all(bind=engine)
    Base.metadata.create_all(bind=engine)
    with TestClient(app) as test_client:
        yield test_client
