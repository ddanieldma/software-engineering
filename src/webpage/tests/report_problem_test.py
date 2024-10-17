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


# Mock function to replace the real database connection
@pytest.fixture
def mock_get_db_connection(monkeypatch):
    class MockCursor:
        def execute(self, query, params):
            # Simulate successful insertion for INSERT INTO problemas_reportados
            if query.startswith("INSERT INTO problemas_reportados"):
                self.successful_insert = True

        def close(self):
            pass

        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc_val, exc_tb):
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

    monkeypatch.setattr('db.get_db_connection', mock_get_db_connection)

# Test submitting a problem report
def test_submit_problem_report(client, mock_get_db_connection):
    with client.session_transaction() as session:
        session['user_id'] = 1  # Mock a logged-in user

    response = client.post('/report-problem', data={
        'tipo_problema': 'Vending Machine',
        'descricao': 'The vending machine is not working.',
        'id_maquina': 101
    }, follow_redirects=True)

    assert response.status_code == 200
    assert b'Problem report submitted successfully!' in response.data
