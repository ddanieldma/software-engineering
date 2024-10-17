import pytest
import sys
import os
from dotenv import load_dotenv
import mysql.connector
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from app import app

load_dotenv()
secret_key = os.getenv('FLASK_SECRET_KEY')
user= os.getenv("MYSQL_USER")
password = os.getenv("MYSQL_PASSWORD")

@pytest.fixture(scope="module")
def db():
    # Establish a connection to the test database
    conn = mysql.connector.connect(
        host="localhost",
        user=user,
        password=password,
        database="coffe_map"
    )
    cursor = conn.cursor()

    # Create necessary tables if they don't exist
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS usuarios (
        id INT AUTO_INCREMENT PRIMARY KEY,
        nome VARCHAR(255) NOT NULL,
        email VARCHAR(255) NOT NULL UNIQUE,
        senha_hash VARCHAR(255) NOT NULL,
        role ENUM('Admin', 'Vendedor', 'Comprador') DEFAULT 'Comprador',
        is_admin BOOLEAN DEFAULT FALSE,
        is_vendedor BOOLEAN DEFAULT FALSE,
        data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
    );
    """)
    
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS problemas_reportados (
        id INT AUTO_INCREMENT PRIMARY KEY,
        id_usuario INT NOT NULL,
        tipo_problema ENUM('Vending Machine', 'Rede Social') NOT NULL,
        descricao TEXT NOT NULL,
        status ENUM('Aberto', 'Em andamento', 'Resolvido') DEFAULT 'Aberto',
        data_report TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
        data_resolucao TIMESTAMP NULL,
        id_maquina INT,
        FOREIGN KEY (id_usuario) REFERENCES usuarios(id)
    );
    """)

    # Insert a user into the usuarios table for testing purposes
    cursor.execute("""
    INSERT INTO usuarios (nome, email, senha_hash, role, is_admin, is_vendedor)
    VALUES ('Test User', 'testuser@example.com', SHA2('password123', 256), 'Comprador', False, False)
    """)
    conn.commit()

    yield conn

    # Clean up - drop tables after testing
    cursor.execute("DROP TABLE problemas_reportados")
    cursor.execute("DROP TABLE usuarios")
    conn.commit()
    cursor.close()
    conn.close()

@pytest.fixture
def client(db):
    app.config['TESTING'] = True
    app.config['SECRET_KEY'] = secret_key

    with app.test_client() as client:
        yield client

# Test if the report problem page loads correctly
def test_report_problem_page_loads(client):
    with client.session_transaction() as session:
        session['user_id'] = 1  # Use a valid user ID

    response = client.get('/report-problem')
    assert response.status_code == 200
    assert b'Report a Problem' in response.data

# Test submitting a problem report
def test_submit_problem_report(client, db):
    with client.session_transaction() as session:
        session['user_id'] = 1  # Use a valid user ID

    response = client.post('/report-problem', data={
        'tipo_problema': 'Vending Machine',
        'descricao': 'The vending machine is not working properly.',
        'id_maquina': 1
    }, follow_redirects=True)

    print(response.data)
    assert response.status_code == 200
    assert b'Problem report submitted successfully!' in response.data