import mysql.connector
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Database credentials
usuario = os.getenv("MYSQL_USER")
senha = os.getenv("MYSQL_PASSWORD")

# Connect to the MySQL database
conexao = mysql.connector.connect(
    host="localhost",
    user=usuario,
    password=senha,
    database="coffe_map"
)

# Create a cursor to execute SQL commands
cursor = conexao.cursor()

cursor.execute("SET FOREIGN_KEY_CHECKS = 0;")  # Desativar verificações de chave estrangeira
cursor.execute("TRUNCATE TABLE produtos;")
cursor.execute("TRUNCATE TABLE vending_machines;")
cursor.execute("TRUNCATE TABLE problemas_reportados;")
cursor.execute("TRUNCATE TABLE usuarios;")
cursor.execute("TRUNCATE TABLE avaliacoes;")
cursor.execute("SET FOREIGN_KEY_CHECKS = 1;")  # Reativar verificações de chave estrangeira

# Populate 'usuarios' table
cursor.execute("""
INSERT INTO usuarios (nome, email, senha_hash, role, is_admin, is_vendedor)
VALUES 
    ('Alice Santos', 'alice@example.com', 'hashed_password_1', 'Admin', TRUE, FALSE),
    ('Bruno Oliveira', 'bruno@example.com', 'hashed_password_2', 'Vendedor', FALSE, TRUE),
    ('Carlos Silva', 'carlos@example.com', 'hashed_password_3', 'Comprador', FALSE, FALSE);
""")

# Populate 'vending_machines' table
cursor.execute("""
INSERT INTO vending_machines (localizacao)
VALUES 
    ('Rua da Praia, 123 - Centro, Porto Alegre'),
    ('Avenida Paulista, 900 - Bela Vista, São Paulo'),
    ('Praça XV, 45 - Centro, Rio de Janeiro');
""")

# Populate 'produtos' table with nutritional information added
cursor.execute("""
INSERT INTO produtos (nome, descricao, preco, estoque, categoria, imagem_url, id_vending_machine)
VALUES 
    ('Café Expresso', 'Café quente e encorpado, servido em um copo pequeno. Informação Nutricional: 2 kcal, 0g gordura, 0g carboidrato, 0g proteína.', 5.00, 100, 'Bebidas', 'https://example.com/cafe_expresso.jpg', 1),
    ('Chá Verde', 'Bebida saudável e refrescante. Informação Nutricional: 0 kcal, 0g gordura, 0g carboidrato, 0g proteína.', 4.50, 80, 'Bebidas', 'https://example.com/cha_verde.jpg', 2),
    ('Biscoito de Chocolate', 'Biscoito crocante com pedaços de chocolate. Informação Nutricional: 120 kcal, 5g gordura, 18g carboidrato, 2g proteína.', 3.00, 120, 'Lanches', 'https://example.com/biscoito_chocolate.jpg', 3);
""")


# Populate 'problemas_reportados' table
cursor.execute("""
INSERT INTO problemas_reportados (id_usuario, tipo_problema, descricao, status, id_maquina)
VALUES 
    (1, 'Vending Machine', 'Máquina não está aceitando pagamentos com cartão', 'Aberto', 1),
    (2, 'Rede Social', 'Dificuldade para acessar minha conta via Facebook', 'Em andamento', NULL),
    (3, 'Vending Machine', 'Produto preso na máquina após pagamento', 'Resolvido', 2);
""")

# Populate 'avaliacoes' table
cursor.execute("""
INSERT INTO avaliacoes (rating, id_maquina)
VALUES 
    (4.5, 1),
    (3.0, 2),
    (5.0, 3);
""")

# Commit the changes

conexao.commit()

# Close the cursor and connection
cursor.close()
conexao.close()

print("Database populated successfully.")
