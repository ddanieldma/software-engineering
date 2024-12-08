import mysql.connector
from dotenv import load_dotenv
import os
import mysql.connector
from faker import Faker
import random
from webpage.app import db

from models import *

# Carregar as variáveis de ambiente do arquivo .env
# load_dotenv()

# usuario = os.getenv("MYSQL_USER")
# senha = os.getenv("MYSQL_PASSWORD")

# Conectar ao banco de dados MySQL
# conexao = mysql.connector.connect(
#     host="localhost",
#     user=usuario,
#     password=senha,
#     database="coffe_map"
# )

# Truncando tabelas para sempre gerar dados novos.
db.session.execute("SET FOREIGN_KEY_CHECKS = 0;")  # Desativar verificações de chave estrangeira
db.session.execute("TRUNCATE TABLE produtos;")
db.session.execute("TRUNCATE TABLE vending_machines;")
db.session.execute("TRUNCATE TABLE problemas_reportados;")
db.session.execute("TRUNCATE TABLE usuarios;")
db.session.execute("TRUNCATE TABLE avaliacoes;")
db.session.execute("SET FOREIGN_KEY_CHECKS = 1;")  # Reativar verificações de chave estrangeira

db.session.commit()

# Inserindo dados fixos
# Usuários
usuario1 = User(nome="Alice Santos", email="alice@example.com", senha_hash="hashed_password_1", role="Admin", is_admin=True, is_vendedor=False)
usuario2 = User(nome="Bruno Oliveira", email="bruno@example.com", senha_hash="hashed_password_2", role="Vendedor", is_admin=False, is_vendedor=True)
usuario3 = User(nome="Carlos Silva", email="carlos@example.com", senha_hash="hashed_password_3", role="Comprador", is_admin=False, is_vendedor=False)
db.session.add_all([usuario1, usuario2, usuario3])

# vending machines
vending_machine = VendingMachine(localizacao="Rua da Praia, 123 - Centro, Porto Alegre")
db.session.add(vending_machine)

# Produtos
produto = Product(
    nome="Café Expresso",
    descricao="Café quente e encorpado, servido em um copo pequeno. Informação Nutricional: 2 kcal, 0g gordura, 0g carboidrato, 0g proteína.",
    preco=5.00,
    estoque=100,
    categoria="Bebidas",
    imagem_url="https://example.com/cafe_expresso.jpg",
    id_vending_machine=1
)
db.session.add(produto)

# Problemas reportados
problema = ReportedProblem(id_usuario=1, tipo_problema="Vending Machine", descricao="Máquina não está aceitando pagamentos com cartão", status="Aberto", id_maquina=1)
db.session.add(problema)

# Avaliações
avaliacao = Rating(rating=4.5, id_maquina=1)
db.session.add(avaliacao)

# Comitando inserções
db.session.commit()


# Instanciar o Faker para gerar dados falsos
faker = Faker()

# Função para gerar usuários falsos
def populate_usuarios(n):
    for _ in range(n):
        nome = faker.name()
        email = faker.email()
        senha_hash = faker.sha256()
        role = random.choice(['Admin', 'Vendedor', 'Comprador'])
        is_admin = True if role == 'Admin' else False
        is_vendedor = True if role == 'Vendedor' else False
        User.create(
            nome = nome,
            email = email,
            senha_hash = senha_hash,
            role = role,
            is_admin = is_admin,
            is_vendedor = is_vendedor
        )

# Função para gerar vending machines falsas
def populate_vending_machines(n):
    for _ in range(n):
        localizacao = faker.address()
        VendingMachine.create(localizacao=localizacao)

def populate_produtos(n):
    cursor.execute("SELECT id FROM vending_machines")
    vending_machines_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(n):
        nome = faker.word()
        descricao = faker.text()
        preco = round(random.uniform(1.0, 100.0), 2)
        estoque = random.randint(1, 100)
        categoria = faker.word()
        imagem_url = faker.image_url()
        id_vending_machine = random.choice(vending_machines_ids) if vending_machines_ids else None
        Product.create(
            nome=nome,
            descricao=descricao,
            preco=preco,
            estoque=estoque,
            categoria=categoria,
            imagem_url=imagem_url,
            id_vending_machine=id_vending_machine
        )
        
# Função para gerar problemas reportados falsos
def populate_problemas_reportados(n):
    cursor.execute("SELECT id FROM usuarios")
    usuarios_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id FROM vending_machines")
    vending_machines_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(n):
        id_usuario = random.choice(usuarios_ids) if usuarios_ids else None
        tipo_problema = random.choice(['Vending Machine', 'Rede Social'])
        descricao = faker.text()
        status = random.choice(['Aberto', 'Em andamento', 'Resolvido'])
        id_maquina = random.choice(vending_machines_ids) if vending_machines_ids else None
        ReportedProblem.create(
            id_usuario = id_usuario,
            tipo_problema = tipo_problema,
            descricao = descricao,
            status = status,
            id_maquina = id_maquina
        )

# Populando as tabelas com dados falsos
populate_usuarios(10)          # 10 usuários
populate_vending_machines(5)   # 5 vending machines
populate_produtos(20)          # 20 produtos
populate_problemas_reportados(15)  # 15 problemas reportados

# # Confirmar as mudanças no banco de dados
# conexao.commit()

# # Fechar o cursor e a conexão
# cursor.close()
# conexao.close()

print("Tabelas populadas com dados falsos e fixos com sucesso.")
