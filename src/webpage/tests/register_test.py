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
