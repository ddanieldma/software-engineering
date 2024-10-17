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

# Test if the report problem page loads correctly
def test_report_problem_page_loads(client):
    with client.session_transaction() as session:
        session['user_id'] = 1  # Mock a logged-in user

    response = client.get('/report-problem')
    assert response.status_code == 200
    assert b'Report a Problem' in response.data  # Check for the text on the page
