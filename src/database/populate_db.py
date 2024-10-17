from dotenv import load_dotenv
import os
import mysql.connector
from faker import Faker
import random

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

usuario = os.getenv("MYSQL_USER")
senha = os.getenv("MYSQL_PASSWORD")

# Conectar ao banco de dados MySQL
conexao = mysql.connector.connect(
    host="localhost",
    user=usuario,
    password=senha,
    database="coffe_map"
)

# Criar um cursor para executar comandos SQL
cursor = conexao.cursor()

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
        cursor.execute("""
            INSERT INTO usuarios (nome, email, senha_hash, role, is_admin, is_vendedor)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (nome, email, senha_hash, role, is_admin, is_vendedor))

# Função para gerar vending machines falsas
def populate_vending_machines(n):
    for _ in range(n):
        localizacao = faker.address()
        cursor.execute("""
            INSERT INTO vending_machines (localizacao)
            VALUES (%s);
        """, (localizacao,))

# Função para gerar produtos falsos
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
        cursor.execute("""
            INSERT INTO produtos (nome, descricao, preco, estoque, categoria, imagem_url, id_vending_machine)
            VALUES (%s, %s, %s, %s, %s, %s, %s);
        """, (nome, descricao, preco, estoque, categoria, imagem_url, id_vending_machine))

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
        cursor.execute("""
            INSERT INTO problemas_reportados (id_usuario, tipo_problema, descricao, status, id_maquina)
            VALUES (%s, %s, %s, %s, %s);
        """, (id_usuario, tipo_problema, descricao, status, id_maquina))

# Populando as tabelas com dados falsos
populate_usuarios(10)          # 10 usuários
populate_vending_machines(5)   # 5 vending machines
populate_produtos(20)          # 20 produtos
populate_problemas_reportados(15)  # 15 problemas reportados

# Confirmar as mudanças no banco de dados
conexao.commit()

# Fechar o cursor e a conexão
cursor.close()
conexao.close()

print("Tabelas populadas com dados falsos com sucesso.")