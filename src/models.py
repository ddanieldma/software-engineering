from webpage.app import db
from sqlalchemy import Enum

# Modelo de produto
class Product(db.Model):
    __tablename__ = 'produtos'

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    descricao = db.Column(db.Text)
    preco = db.Column(db.Numeric(10, 2), nullable=False)
    estoque = db.Column(db.Integer, nullable=False)
    categoria = db.Column(db.String(255))
    imagem_url = db.Column(db.String(255))
    data_criacao = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    id_vending_machine = db.Column(db.Integer, db.ForeignKey('vending_machines.id'))

    def __repr__(self):
        return f"<Product {self.nome}, {self.preco}, {self.estoque}>"

    @classmethod
    def create(cls, nome, descricao, preco, estoque, categoria, imagem_url, vending_machine_id):
        product = cls(
            nome=nome,
            descricao=descricao,
            preco=preco,
            estoque=estoque,
            categoria=categoria,
            imagem_url=imagem_url,
            id_vending_machine=vending_machine_id
        )
        db.session.add(product)
        db.session.commit()
        return product

# Classe construtora do produto
class ProductBuilder:
    """
    Builder for creating a Product with specific attributes.

    Provides methods to set each field do produto step by step
    """

    def __init__(self):
        self.nome = None
        self.descrição = None
        self.preco = None
        self.estoque = None
        self.categoria = None
        self.imagem_url = None
        self.vending_machine_id = None

    def set_nome(self, nome):
        """
        Sets the nome do produto.

        Args:
            nome (str): The nome do produto.

        Returns:
            self (ProductBuilder): The current instance for method chaining.
        """
        self.nome = nome
        return self
        
    def set_descrição(self, descrição):
        """
        Sets the descrição do produto.

        Args:
            descrição (str): The descrição do produto.

        Returns:
            self (ProductBuilder): The current instance for method chaining.
        """
        self.descrição = descrição
        return self
    
    def set_preco(self, preco):
        """
        Sets the preco do produto.

        Args:
            preco (int): The preco do produto.

        Returns:
            self (ProductBuilder): The current instance for method chaining.
        """
        self.preco = preco
        return self
    
    def set_estoque(self, estoque):
        """
        Sets the estoque do produto.

        Args:
            estoque (int): The estoque do produto.

        Returns:
            self (ProductBuilder): The current instance for method chaining.
        """
        self.estoque = estoque
        return self
    
    def set_categoria(self, categoria):
        """
        Sets the categoria do produto.

        Args:
            categoria (str): The categoria do produto.

        Returns:
            self (ProductBuilder): The current instance for method chaining.
        """
        self.categoria = categoria
        return self
    
    def set_imagem_url(self, imagem_url):
        """
        Sets the imagem_url do produto.

        Args:
            imagem_url (str): The imagem_url do produto.

        Returns:
            self (ProductBuilder): The current instance for method chaining.
        """
        self.imagem_url = imagem_url
        return self
    
    def set_vending_machine_id(self, vending_machine_id):
        """
        Sets the vending_machine_id do produto.

        Args:
            vending_machine_id (int): The vending_machine_id do produto.

        Returns:
            self (ProductBuilder): The current instance for method chaining.
        """
        self.vending_machine_id = vending_machine_id
        return self
    
    def build(self):
        """
        Returns a fully constructed Product object using the provided attributes

        Returns:
            Product: The newly created object
        """

        # Ensure all required fields are set
        if None in [self.nome, self.descrição, self.preco, self.estoque, self.categoria, self.imagem_url, self.vending_machine_id]:
            raise ValueError("Missing required product attribute.")

        return Product(self.nome, self.descrição, self.preco, self.estoque, self.categoria, self.imagem_url, self.vending_machine_id)


# Modelo de usuário
class User(db.Model):
    __tablename__ = 'usuarios'  # Table name in the database

    id = db.Column(db.Integer, primary_key=True)
    nome = db.Column(db.String(255), nullable=False)
    email = db.Column(db.String(255), unique=True, nullable=False)
    senha_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(Enum('Admin', 'Vendedor', 'Comprador', name='role_enum'), default='Comprador')
    is_admin = db.Column(db.Boolean, default=False)
    is_vendedor = db.Column(db.Boolean, default=False)
    data_criacao = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    def __repr__(self):
        return f"<User {self.nome}, {self.email}>"

    @classmethod
    def create(cls, nome, email, senha_hash, role='Comprador', is_admin=False, is_vendedor=False):
        user = cls(
            nome=nome,
            email=email,
            senha_hash=senha_hash,
            role=role,
            is_admin=is_admin,
            is_vendedor=is_vendedor
        )
        db.session.add(user)
        db.session.commit()
        return user


# Modelo de máquina de vendas
class VendingMachine(db.Model):
    __tablename__ = 'vending_machines'

    id = db.Column(db.Integer, primary_key=True)
    localizacao = db.Column(db.String(255), nullable=False)
    data_instalacao = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())

    produtos = db.relationship('Product', backref='vending_machine', lazy=True)  # Relationship with products

    def __repr__(self):
        return f"<VendingMachine {self.localizacao}>"

    @classmethod
    def create(cls, localizacao):
        vending_machine = cls(localizacao=localizacao)
        db.session.add(vending_machine)
        db.session.commit()
        return vending_machine


# Modelo de problema reportado
class ReportedProblem(db.Model):
    __tablename__ = 'problemas_reportados'

    id = db.Column(db.Integer, primary_key=True)
    id_usuario = db.Column(db.Integer, db.ForeignKey('usuarios.id'), nullable=False)
    tipo_problema = db.Column(Enum('Vending Machine', 'Rede Social', name='problem_type_enum'), nullable=False)
    descricao = db.Column(db.Text, nullable=False)
    status = db.Column(Enum('Aberto', 'Em andamento', 'Resolvido', name='status_enum'), default='Aberto')
    data_report = db.Column(db.TIMESTAMP, default=db.func.current_timestamp())
    data_resolucao = db.Column(db.TIMESTAMP, nullable=True)
    id_maquina = db.Column(db.Integer, db.ForeignKey('vending_machines.id'))

    usuario = db.relationship('User', backref='problemas_reportados', lazy=True)
    maquina = db.relationship('VendingMachine', backref='problemas_reportados', lazy=True)

    def __repr__(self):
        return f"<ReportedProblem {self.tipo_problema}, {self.status}>"

    @classmethod
    def create(cls, id_usuario, tipo_problema, descricao, id_maquina, status='Aberto'):
        problem = cls(
            id_usuario=id_usuario,
            tipo_problema=tipo_problema,
            descricao=descricao,
            id_maquina=id_maquina,
            status=status
        )
        db.session.add(problem)
        db.session.commit()
        return problem

class Rating(db.Model):
    __tablename__ = 'avaliacoes'

    id = db.Column(db.Integer, primary_key=True)
    rating = db.Column(db.Numeric(2, 1), nullable=False)
    id_maquina = db.Column(db.Integer, db.ForeignKey('vending_machines.id'), nullable=False)

    maquina = db.relationship('VendingMachine', backref='avaliacoes', lazy=True)

    def __repr__(self):
        return f"<Rating {self.rating}, VendingMachine {self.id_maquina}>"

    @classmethod
    def create(cls, rating, id_maquina):
        rating_instance = cls(
            rating=rating,
            id_maquina=id_maquina
        )
        db.session.add(rating_instance)
        db.session.commit()
        return rating_instance

def save_product(product):
    saved_product = Product.create(
        product.nome, product.descrição, product.preco, 
        product.estoque, product.categoria, product.imagem_url, 
        product.vending_machine_id
    )

    print(saved_product)

if __name__ == '__main__':
    # Instanciando um produto com builder
    soda_can = (ProductBuilder()
                .set_nome("Soda Can")
                .set_descrição("A refreshing soda can")
                .set_preco(2.5)
                .set_estoque(100)
                .set_categoria("Beverages")
                .set_imagem_url("url")
                .set_vending_machine_id(1)
                .build())
    
    print(soda_can)

    # Adicionando produto na base de dados
    save_product(soda_can)

    # Fazendo query de todos os produtos
    all_products = Product.query.all()

    # query por nome
    product = Product.query.filter_by(nome="Soda Can").first()

    # Atualizando um produto
    product = Product.query.filter_by(id=1).first()
    if product:
        product.preco = 2.75
        db.session.commit()

    # Deletando um produto
    product = Product.query.filter_by(id=1).first()
    if product:
        db.session.delete(product)
        db.session.commit()
