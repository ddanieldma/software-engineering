import pytest
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app


@pytest.fixture
def client():
    app.config['TESTING'] = True
    with app.test_client() as client:
        yield client

def test_register_page_loads(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register User' in response.data  # Check if the form text is present

def test_register_user(client, monkeypatch):
    # Mock the database connection and cursor
    def mock_get_db_connection():
        class MockCursor:
            def execute(self, query, params):
                pass
            def close(self):
                pass
        class MockConnection:
            def cursor(self):
                return MockCursor()
            def commit(self):
                pass
            def close(self):
                pass
        return MockConnection()

    monkeypatch.setattr('db.get_db_connection', mock_get_db_connection)

    response = client.post('/register', data={
        'nome': 'Test User',
        'email': 'test@example.com',
        'senha': 'password123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'User registered successfully!' in response.data
