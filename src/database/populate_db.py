import mysql.connector
from dotenv import load_dotenv
import os
import random
from faker import Faker

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

usuario = os.getenv("MYSQL_USER")
senha = os.getenv("MYSQL_PASSWORD")

# Conectar ao banco de dados MySQL
conexao = mysql.connector.connect(
    host="localhost",
    user=usuario,  # Substitua pelo seu usuário MySQL
    password=senha,  # Substitua pela sua senha MySQL
    database="coffe_map"  # Nome do banco de dados onde as tabelas serão criadas
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

# Função para gerar ratings de vending machines
def populate_ratings(n):
    cursor.execute("SELECT id FROM vending_machines")
    vending_machines_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(n):
        rating = round(random.uniform(0, 5), 1)
        id_maquina = random.choice(vending_machines_ids)
        cursor.execute("""
            INSERT INTO ratings (rating, id_maquina)
            VALUES (%s, %s);
        """, (rating, id_maquina))

# Função para gerar máquinas favoritas dos usuários
def populate_favoritos(n):
    cursor.execute("SELECT id FROM usuarios")
    usuarios_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id FROM vending_machines")
    vending_machines_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(n):
        id_usuario = random.choice(usuarios_ids)
        id_maquina = random.choice(vending_machines_ids)
        is_favorite = random.choice([True, False])
        cursor.execute("""
            INSERT INTO favoritos (id_usuario, id_maquina, is_favorite)
            VALUES (%s, %s, %s);
        """, (id_usuario, id_maquina, is_favorite))

# Função para gerar compras
def populate_compras(n):
    cursor.execute("SELECT id FROM usuarios")
    usuarios_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id FROM produtos")
    produtos_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id FROM vending_machines")
    vending_machines_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(n):
        user_id = random.choice(usuarios_ids)
        product_id = random.choice(produtos_ids)
        product_price = round(random.uniform(1.0, 100.0), 2)
        machine_id = random.choice(vending_machines_ids)
        cursor.execute("""
            INSERT INTO compras (user_id, product_name, product_price, machine_id)
            VALUES (%s, %s, %s, %s);
        """, (user_id, faker.word(), product_price, machine_id))

# Função para gerar avaliações
def populate_avaliacoes(n):
    cursor.execute("SELECT id FROM usuarios")
    usuarios_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id FROM produtos")
    produtos_ids = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT id FROM vending_machines")
    vending_machines_ids = [row[0] for row in cursor.fetchall()]

    for _ in range(n):
        id_usuario = random.choice(usuarios_ids)
        id_produto = random.choice(produtos_ids)
        id_maquina = random.choice(vending_machines_ids)
        nota_maquina = random.randint(1, 5)
        nota_produto = random.randint(1, 5)
        comentario = faker.text(max_nb_chars=140)
        cursor.execute("""
            INSERT INTO avaliacoes (id_usuario, id_maquina, id_produto, nota_maquina, nota_produto, comentario)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (id_usuario, id_maquina, id_produto, nota_maquina, nota_produto, comentario))

# Populando as tabelas com dados falsos
populate_usuarios(10)          # 10 usuários
populate_vending_machines(5)   # 5 vending machines
populate_produtos(20)          # 20 produtos
populate_problemas_reportados(15)  # 15 problemas reportados
populate_ratings(10)           # 10 ratings
populate_favoritos(15)         # 15 favoritos
populate_compras(25)           # 25 compras
populate_avaliacoes(30)        # 30 avaliações

# Confirmar as mudanças no banco de dados
conexao.commit()

# Fechar o cursor e a conexão
cursor.close()
conexao.close()

print("Tabelas populadas com dados falsos e fixos com sucesso.")
