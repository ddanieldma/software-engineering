from dotenv import load_dotenv
import os
import mysql.connector

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

# Criar tabela de usuários
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

# Criar tabela de vending machines
cursor.execute("""
CREATE TABLE IF NOT EXISTS vending_machines (
    id INT AUTO_INCREMENT PRIMARY KEY,
    localizacao VARCHAR(255) NOT NULL,
    data_instalacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);
""")

# Criar tabela de produtos
cursor.execute("""
CREATE TABLE IF NOT EXISTS produtos (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(255) NOT NULL,
    descricao TEXT,
    preco DECIMAL(10, 2) NOT NULL,
    estoque INT NOT NULL,
    categoria VARCHAR(255),
    imagem_url VARCHAR(255),
    data_criacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    id_vending_machine INT,
    FOREIGN KEY (id_vending_machine) REFERENCES vending_machines(id)
);
""")

# Criar tabela de problemas reportados
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
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (id_maquina) REFERENCES vending_machines(id)
);
""")

# Criar tabela de ratings
cursor.execute("""
CREATE TABLE IF NOT EXISTS avaliacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    rating DECIMAL(2, 1) NOT NULL CHECK (rating >= 0 AND rating <= 5),  # Valores de 0.0 a 5.0
    id_maquina INT NOT NULL,
    FOREIGN KEY (id_maquina) REFERENCES vending_machines(id)
);
""")

# Criar tabela de avaliações
cursor.execute("""
CREATE TABLE IF NOT EXISTS avaliacoes (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_usuario INT NOT NULL,
    id_maquina INT NOT NULL,
    id_produto INT NOT NULL,
    nota_maquina DECIMAL(2, 1) NOT NULL CHECK (nota_maquina >= 0 AND nota_maquina <= 5), -- Nota de 0.0 a 5.0
    nota_produto DECIMAL(2, 1) NOT NULL CHECK (nota_produto >= 0 AND nota_produto <= 5), -- Nota de 0.0 a 5.0
    data_avaliacao TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    comentario TEXT,
    FOREIGN KEY (id_usuario) REFERENCES usuarios(id),
    FOREIGN KEY (id_maquina) REFERENCES vending_machines(id),
    FOREIGN KEY (id_produto) REFERENCES produtos(id)
               
);
""")


# Confirmar as mudanças no banco de dados
conexao.commit()

# Fechar o cursor e a conexão
cursor.close()
conexao.close()

print("Tabelas criadas com sucesso no banco de dados 'coffee_map'.")
