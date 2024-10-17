import os
import pytest
import sys
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

from dotenv import load_dotenv

load_dotenv()

@pytest.fixture
def client():
    from app import app  # Import app here to avoid circular import issues
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = os.getenv('FLASK_SECRET_KEY')
    with app.test_client() as client:
        yield client

def test_register_page_loads(client):
    response = client.get('/register')
    assert response.status_code == 200
    assert b'Register User' in response.data  # Check if the form text is present

# Import app AFTER monkeypatch is applied
def test_register_user(monkeypatch):
    # Simplified mock of database connection and cursor
    class MockCursor:
        def execute(self, query, params):
            print(f"Mock execute called with query: {query}, params: {params}")
            pass  # Mock execute does nothing for the test
        def close(self):
            pass

    class MockConnection:
        def cursor(self):
            return MockCursor()
        def commit(self):
            pass
        def close(self):
            pass

    def mock_get_db_connection():
        return MockConnection()

    # Apply the monkeypatch
    monkeypatch.setattr('db.get_db_connection', mock_get_db_connection)

    # Import app AFTER patching
    from app import app

    secret_key = os.getenv('FLASK_SECRET_KEY')
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = secret_key # Set secret key for testing

    with app.test_client() as client:
        response = client.post('/register', data={
            'nome': 'Test User',
            'email': 'test@example.com',
            'senha': 'password123'
        }, follow_redirects=True)

        print(response.data)
        # Assert that the flash message indicating success is in the response
        assert b'Successfully! registered' in response.data  # Adjust the message as per your app's response

