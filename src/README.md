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

ADMIN_PASSWORD=some_password &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;  # Uma senha qualquer que vai te permitir criar contas de admin na interface do site.


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

Em geral os dados fictícios são aleatórios, mas você pode criar contas de admin com a senha de admin que você vai selecionar


Após o banco de dados e tabelas terem sido criados e populados você deve executar o `app.py`

```bash
python webpage/app.py
```

E então abrir o localhost na porta 5000. A partir desse ponto a exploração da aplicação fica a critério do usuário.


O relatório do projeto pode ser encontrado [Aqui.](https://drive.google.com/file/d/1U_IiqyixMoM4e7UEmPZl9ncP_E7ku_F0/view?usp=sharing)
