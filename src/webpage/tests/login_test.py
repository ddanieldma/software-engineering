import pytest
import sys
import os
from dotenv import load_dotenv
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

load_dotenv()
secret_key = os.getenv('FLASK_SECRET_KEY')

@pytest.fixture
def client():
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = secret_key
    with app.test_client() as client:
        yield client

# Test if the login page loads correctly
def test_login_page_loads(client):
    response = client.get('/login')
    assert response.status_code == 200
    assert b'Login' in response.data  # Verify if 'Login' text is present in the response

import hashlib

# Mock function to replace the real database connection
@pytest.fixture
def mock_get_db_connection(monkeypatch):
    class MockCursor:
        def execute(self, query, params):
            if query.startswith("SELECT * FROM usuarios"):
                # Simulate a successful user retrieval
                email, password_hash = params
                if email == 'test@example.com' and password_hash == hashlib.sha256('password123'.encode()).hexdigest():
                    self.result = [(1, 'Test User', 'test@example.com', password_hash)]
                else:
                    self.result = []

        def fetchone(self):
            return self.result[0] if self.result else None

        def close(self):
            pass

    class MockConnection:
        def cursor(self):
            return MockCursor()
        def close(self):
            pass

    def mock_get_db_connection():
        return MockConnection()

    monkeypatch.setattr('db.get_db_connection', mock_get_db_connection)

# Test user login with correct credentials
def test_login_user_success(client, mock_get_db_connection):
    response = client.post('/login', data={
        'email': 'test@example.com',
        'password': 'password123'
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Login successful!' in response.data
