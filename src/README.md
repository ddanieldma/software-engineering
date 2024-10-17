# Projeto: Sistema de Vending Machines

## Pré-requisitos

### Instalação do MySQL Server

Para executar este projeto, é necessário ter o **MySQL Server** instalado. Você pode baixá-lo na versão **full** através do link abaixo:

[Baixar MySQL Server](https://dev.mysql.com/downloads/file/?id=534097)

### Instalação das Dependências

Depois de instalar o MySQL Server, é necessário instalar as dependências do projeto, que estão especificadas no arquivo `requirements.txt` localizado na pasta `src`.

Para instalar as dependências, execute o seguinte comando no terminal dentro da pasta `src`:

```bash
pip install -r requirements.txt
```

Preparação do banco de dados

Crie um arquivo .env com as seguintes váriaveis

MYSQL_USER=root         &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;       # Padrão do MySQL ou outro usuário criado durante a instalação

MYSQL_PASSWORD=sua_senha   &nbsp;&nbsp;&nbsp;    # A senha criada durante a instalação do MySQL

FLASK_SECRET_KEY=secret    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;    # Qualquer chave desejada para a aplicação Flask


Em seguida execute os arquivos na pasta database na seguinte ordem

create_db.py

```bash
python database/create_db.py
```
create_tables.py
```bash
python database/create_tables.py
```

populate_db.py
```bash
python database/populate_db.py
```

Com isso você terá populado o database com dados fictícios.

Em geral os dados fictícios são aleatórios, mas os seguintes logins estarão presentes:

Login de Admin

Nome: 'Alice Santos', 

E-mail: 'alice@example.com', 

Senha: 'hashed_password_1',

Login de User normal

Nome: 'Carlos Silva', 

E-mail: 'carlos@example.com', 

Senha: 'hashed_password_3',

Também teremos a seguinte entrada de vending machine

Entrada de vending machine

Id: 1

Localização: Rua da Praia, 123 - Centro, Porto Alegre

Use o id dessa vending machine na página de reporte de problemas para evitar erros do banco de dados.

Após o banco de dados e tabelas terem sido criados e populados você deve executar o `app.py`

```bash
python webpage/app.py
```

E então abrir o localhost na porta 5000. A partir desse ponto a exploração da aplicação fica a critério do usuário.
