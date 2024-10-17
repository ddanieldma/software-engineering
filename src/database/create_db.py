from dotenv import load_dotenv
import os
import mysql.connector

# Carregar as variáveis de ambiente do arquivo .env
load_dotenv()

usuario = os.getenv("MYSQL_USER")
senha = os.getenv("MYSQL_PASSWORD")

conexao = mysql.connector.connect(
    host="localhost",
    user=usuario,
    password=senha)


# Criando um cursor para executar comandos SQL
cursor = conexao.cursor()

# Criando um banco de dados
cursor.execute("CREATE DATABASE IF NOT EXISTS coffe_map")

# Selecionando o banco de dados recém-criado
cursor.execute("USE coffe_map")

# Fechando o cursor e a conexão
cursor.close()
conexao.close()

