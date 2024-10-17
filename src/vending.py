from abc import ABC, abstractmethod
from collections import defaultdict
from database_managment import DBConnection


class Product:
    """
    Represents a product available in a vending machine.

    Attributes:
        _name (str): The name of the product.
        _id_vending_machine (int): The ID of the vending machine containing the product.
        _description (str): The product's description.
        _price (float): The price of the product.
        _category (str): The category of the product.
        _img_url (str): The URL of the product's image (optional).

    Methods:
        load_from_db(): Loads the product details from the database.
        get_description(): Returns the description of the product.
        set_price(price): Sets the price of the product.
        get_price(): Returns the price of the product.
        get_name(): Returns the name of the product.
        get_category(): Returns the product's category.
        get_img_url(): Returns the product's image URL.
    """
    
    def __init__(self, name, id_vending_machine):
        """
        Initializes the Product instance.

        Args:
            name (str): The name of the product.
            id_vending_machine (int): The ID of the vending machine containing the product.
        """
        self._name = name
        self._id_vending_machine = id_vending_machine
        self._description = None
        self._price = None
        self._category = None
        self._img_url = None

    def load_from_db(self):
        """
        Loads product details from the database.

        Raises:
            ValueError: If the product is not found in the vending machine.
        """
        query = """
        SELECT descricao, preco, categoria, imagem_url FROM produtos
        WHERE nome = %s AND id_vending_machine = %s
        """
        result = DBConnection().execute_query(query, (self._name, self._id_vending_machine))

        if result:
            self._description, self._price, self._category, self._img_url = result
        else:
            raise ValueError(f"Product '{self._name}' not found in vending machine {self._id_vending_machine}.")

    def get_description(self):
        """
        Retrieves the product's description.

        Returns:
            str: The product description.
        """
        if self._description is None:
            self.load_from_db()

        return self._description    

    def set_price(self, price):
        """
        Updates the price of the product in the database.

        Args:
            price (float): The new price to set.

        Raises:
            ValueError: If the price is not a positive number.
        """
        if not isinstance(price, (int, float)):
            raise ValueError('Price must be a number')
        elif price <= 0:
            raise ValueError('Price must be positive')

        query = """
        UPDATE produtos SET preco = %s
        WHERE nome = %s AND id_vending_machine = %s
        """
        DBConnection().execute_query(query, (price, self._name, self._id_vending_machine))

    def get_price(self):
        """
        Retrieves the current price of the product.

        Returns:
            float: The product's price.

        Raises:
            ValueError: If the price has not been set in the database.
        """
        if self._price is None:
            self.load_from_db()

        return self._price

    def get_name(self):
        """
        Retrieves the name of the product.

        Returns:
            str: The product name.
        """
        return self._name

    def get_category(self):
        """
        Retrieves the category of the product.

        Returns:
            str: The category name.
        """
        if self._category is None:
            self.load_from_db()

        return self._category

    def get_img_url(self):
        """
        Retrieves the URL of the product's image.

        Returns:
            str: The image URL.
        """
        if self._img_url is None:
            self.load_from_db()
        return self._img_url

    def __repr__(self):
        """
        Provides a string representation of the product.

        Returns:
            str: The product's name and vending machine ID.
        """
        return self._name


# Vending place superclass
class VendingPlace(ABC):
    """
    Abstract class representing a vending place.

    Attributes:
        _location (str): The location of the vending place.

    Methods:
        get_location(): Returns the location of the vending place.
        get_stock(product): Abstract method to get the stock of a specific product.
        set_stock(product, quantity): Abstract method to set the stock of a specific product.
        add_stock(product, quantity): Adds stock of a product to the vending place.
        simulate_purchase(product, quantity): Simulates a purchase by checking stock and calculating the cost.
    """
    def __init__(self, location):
        """
        Initializes the VendingPlace instance with a location.
        
        Args:
            location (str): The location of the vending place.
        """
        self._location = location

    def get_location(self):
        """
        Gets the location of the vending place.
        
        Returns:
            str: The location of the vending place.
        """
        return self._location

    @abstractmethod
    def get_stock(self):
        """
        Abstract method to get the stock of a specific product.
        
        Returns:
            int: The current stock of the product.

        Raises:
            NotImplementedError: This method must be overridden by subclasses.
        """
        pass

    @abstractmethod
    def set_stock(self):
        """
        Abstract method to set the stock of a specific product.
        
        Raises:
            NotImplementedError: This method must be overridden by subclasses.
        """
        pass

    def add_stock(self, product, quantity):
        """
        Adds stock of a product to the vending place.

        Args:
            product (Product): The product to add stock for.
            quantity (int): The quantity of the product to add.

        Raises:
            ValueError: If the product is not a Product instance or the quantity is negative.
        """
        self._validate_product(product)
        self._validate_quantity(quantity)

        new_quantity = self.get_stock(product) + quantity
        self.set_stock(product, new_quantity)

    def simulate_purchase(self, product, quantity):
        """
        Simulates a purchase by checking stock and calculating the cost.

        Args:
            product (Product): The product to purchase.
            quantity (int): The quantity of the product to purchase.

        Returns:
            float: The total cost of the purchase.

        Raises:
            ValueError: If the product is not valid, if the quantity is not valid, or if there is insufficient stock.
        """
        self._validate_product(product)
        self._validate_quantity(quantity)

        if self.get_stock(product) < quantity:
            raise ValueError(f'Not enough stock! {quantity} requested but only {self.get_stock(product)} available')
        
        return product.get_price() * quantity
        
    def _validate_product(self, product):
        """
        Ensure the product is a Product instance.

        Args:
            product (Product): The product to validate.

        Raises:
            ValueError: If the product is not a Product instance.
        """
        if not isinstance(product, Product):
            raise ValueError('Product must be a Product instance')

    def _validate_quantity(self, quantity):
        """
        Ensure the quantity is a non-negative integer.

        Args:
            quantity (int): The quantity to validate.

        Raises:
            ValueError: If the quantity is not an integer or is negative.
        """
        if not isinstance(quantity, int):
            raise ValueError('Quantity must be an integer')
        elif quantity < 0:
            raise ValueError('Quantity must be non-negative')

class VendingMachine:
    """
    Represents a vending machine at a specific location.

    Attributes:
        _location (str or None): The location of the vending machine. 
        _stock (defaultdict): A cache of the product stock for this vending machine.
        _id (int): The ID of the vending machine.
    
    Methods:
        get_location: Returns the location of the vending machine.
        get_stock: Returns the stock of a specific product or all stock.
        set_stock: Sets the stock of a specific product and updates the database.
    """
    def __init__(self, id: int):
        """
        Initializes the VendingMachine instance with the machine's ID and an empty stock cache.
        
        Args:
            id (int): The ID of the vending machine in the database.
        """
        self._location: str | None = None
        self._id: int = id
        self._stock: defaultdict = defaultdict(int)  # Cache for product stock

    def get_id(self) -> int:
        """
        Returns the ID of the vending machine.
        
        Returns:
            int: The ID of the vending machine.
        """
        return self._id

    def get_location(self) -> str:
        """
        Retrieves the location of the vending machine from the database.
        
        Returns:
            str: The location of the vending machine.
        
        Raises:
            ValueError: If the vending machine is not found in the database.
        """
        if self._location is None:
            # Query to fetch the location of the vending machine
            query = "SELECT localizacao FROM vending_machines WHERE id = %s"
            result = DBConnection().execute_query(query, (self._id,))

            if result:
                self._location = result[0]
            else:
                raise ValueError(f"Vending machine with ID {self._id} not found.")
        
        return self._location

    def get_stock(self, product: str | None = None) -> dict | int:
        """
        Retrieves the stock for a specific product or all products in the vending machine.
        
        Args:
            product (str or None): The name of the product to check stock for. If None, returns all stock.
        
        Returns:
            dict or int: A dictionary with all products and their stock if product is None, or the stock of a specific product.
        
        Raises:
            ValueError: If the specified product is not found in the vending machine.
        """
        if product is None:
            return self._get_all_stock()
        else:
            return self._get_stock_for_product(product)

    def _get_all_stock(self) -> dict:
        """
        Fetches and returns the stock of all products in the vending machine from the database.
        
        Returns:
            dict: A dictionary with products as keys and their stock as values.
        """
        query = """
        SELECT nome, estoque FROM produtos WHERE id_vending_machine = %s
        """
        result = DBConnection().execute_query(query, (self._id,), fetch_all=True)

        # Update local stock cache
        self._stock = defaultdict(int, {Product(name, self._id): stock for name, stock in result})

        return dict(self._stock)
    
    def _get_stock_for_product(self, product: str) -> int:
        """
        Fetches and returns the stock of a specific product from the database.
        
        Args:
            product (str): The name of the product to fetch stock for.
        
        Returns:
            int: The stock quantity of the specified product.
        
        Raises:
            ValueError: If the product is not found in this vending machine.
        """
        query = """
        SELECT estoque FROM produtos WHERE id_vending_machine = %s AND nome = %s
        """
        result = DBConnection().execute_query(query, (self._id, product))

        if result:
            self._stock[product] = result[0]
            return self._stock[product]
        else:
            raise ValueError(f"Product '{product}' not found in this vending machine.")

    def set_stock(self, product: str, quantity: int) -> None:
        """
        Sets the stock for a specific product and updates the database.
        
        Args:
            product (str): The name of the product to update.
            quantity (int): The quantity to set for the product.
        
        Raises:
            ValueError: If the product is not found in the database or if the quantity is invalid.
        """
        self._validate_quantity(quantity)

        # Update the stock in the database
        query = "UPDATE produtos SET estoque = %s WHERE id_vending_machine = %s AND nome = %s"
        result = DBConnection().execute_query(query, (quantity, self._id, product))

        if result.rowcount == 0:
            raise ValueError(f"Product '{product}' not found in this vending machine.")
        
        # Update the local stock cache
        self._stock[product] = quantity

    def _validate_quantity(self, quantity: int) -> None:
        """
        Validates that the provided quantity is a non-negative integer.
        
        Args:
            quantity (int): The quantity to validate.
        
        Raises:
            ValueError: If the quantity is not a non-negative integer.
        """
        if not isinstance(quantity, int) or quantity < 0:
            raise ValueError("Quantity must be a non-negative integer.")

    def __repr__(self) -> str:
        """
        Returns a string representation of the vending machine, including its ID and location.
        
        Returns:
            str: A string describing the vending machine.
        """
        return f"Vending Machine {self._id} at {self.get_location()}"


# Student vending class
class StudentVending(VendingMachine):
    """
    Represents a student-run vending machine, allowing students to sell their own products.

    Inherits from VendingMachine.

    Attributes:
        _student_id (str): The ID of the student running the vending machine.
        _product (Product): The product being sold by the student.
        _stock (int): The stock of the product being sold.

    Methods:
        get_student_id(): Returns the student ID.
        set_product(product): Sets the product the student is selling.
        get_product(): Returns the product the student is selling.
        set_stock(product, quantity): Sets the stock of the student's product.
        get_stock(product): Gets the stock of the student's product.
    """
    def __init__(self, location, student_id):
        """
        Initializes the StudentVending instance with a location and student ID.
        
        Args:
            location (str): The location of the student vending machine.
            student_id (str): The ID of the student running the vending machine.
        """
        super().__init__(location)
        self._student_id = student_id
        self._product = None
        self._stock = 0

    def get_student_id(self):
        """
        Gets the student ID of the vending machine operator.
        
        Returns:
            str: The student ID.
        """
        return self._student_id
    
    def set_product(self, product):
        """
        Sets the product being sold by the student.

        Args:
            product (Product): The product to be sold.

        Raises:
            ValueError: If the product is not a Product instance.
        """
        if not isinstance(product, Product):
            raise ValueError('Product must be a Product instance')

        self._product = product

    def get_product(self):
        """
        Gets the product being sold by the student.
        
        Returns:
            Product: The product being sold.
        """
        return self._product
    
    def set_stock(self, product, quantity):
        """
        Sets the stock of the product being sold by the student.

        Args:
            product (Product): The product to set stock for.
            quantity (int): The quantity to set.

        Raises:
            ValueError: If the product is not the student's product or if the quantity is invalid.
        """
        if product != self._product:
            raise ValueError('This student does not sell this product')
        
        self._validate_quantity(quantity)
        self._stock = quantity
    
    def get_stock(self, product):
        """
        Gets the stock of the product being sold by the student.

        Args:
            product (Product): The product to get stock for.

        Returns:
            int: The current stock of the product.

        Raises:
            ValueError: If the product is not the student's product.
        """
        if product != self._product:
            raise ValueError('This student does not sell this product')
        
        return self._stock


if __name__ == '__main__':
    # Create Vending Machine instance
    vending_machine = VendingMachine(1)
    print(vending_machine.get_location())

    # Get stock of all products
    print(vending_machine.get_stock())

    # Get stock of a specific product
    print(vending_machine.get_stock('change'))

    product = Product('change', 1)

    print("Product price:", product.get_price())

    # Set price of the product
    product.set_price(2)
    print("Product price after setting:", product.get_price())