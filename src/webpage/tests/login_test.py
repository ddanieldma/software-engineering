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
