from abc import ABC, abstractmethod
from collections import defaultdict

# Product class
class Product:
    """
    Represents a product with a name and price.

    Attributes:
        _name (str): The name of the product.
        _price (float): The price of the product, initially set to None.

    Methods:
        set_price(price): Sets the price of the product.
        get_price(): Returns the price of the product. Raises an error if the price is not set.
        get_name(): Returns the name of the product.
    """
    def __init__(self, name):
        """
        Initializes the Product instance with a name.
        
        Args:
            name (str): The name of the product.
        """
        self._name = name
        self._price = None

    def set_price(self, price):
        """
        Sets the price of the product.
        
        Args:
            price (float or int): The price to set. Must be positive.

        Raises:
            ValueError: If the price is not a number or is non-positive.
        """
        if not isinstance(price, (int, float)):
            raise ValueError('Price must be a number')
        elif price <= 0:
            raise ValueError('Price must be positive')
        
        self._price = price

    def get_price(self):
        """
        Gets the price of the product.
        
        Returns:
            float: The price of the product.

        Raises:
            ValueError: If the price has not been set.
        """
        if self._price is None:
            raise ValueError('Price is not set')
        
        return self._price
    
    def get_name(self):
        """
        Gets the name of the product.
        
        Returns:
            str: The name of the product.
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

# Vending machine class
class VendingMachine(VendingPlace):
    """
    Represents a vending machine at a specific location.

    Inherits from VendingPlace.

    Attributes:
        _stock (defaultdict): A dictionary holding the stock of products.

    Methods:
        get_stock(product): Returns the stock of a product.
        set_stock(product, quantity): Sets the stock of a product.
    """
    def __init__(self, location):
        """
        Initializes the VendingMachine instance with a location and an empty stock.
        
        Args:
            location (str): The location of the vending machine.
        """
        super().__init__(location)
        self._stock = defaultdict(int)

    def get_stock(self, product):
        """
        Gets the stock of a specific product in the vending machine.
        
        Args:
            product (Product): The product to check stock for.

        Returns:
            int: The current stock of the product.

        Raises:
            ValueError: If the product is not a valid Product instance.
        """
        self._validate_product(product)
        return self._stock[product]
    
    def set_stock(self, product, quantity):
        """
        Sets the stock of a specific product in the vending machine.
        
        Args:
            product (Product): The product to set stock for.
            quantity (int): The quantity to set.

        Raises:
            ValueError: If the product is not valid or if the quantity is invalid.
        """
        self._validate_product(product)
        self._validate_quantity(quantity)

        self._stock[product] = quantity


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

def get_products_from_db():
    coke_product = Product('Coke')
    coke_product.set_price(8)
    brownie_product = Product('Brownie')
    brownie_product.set_price(5)
    return [coke_product, brownie_product]

if __name__ == '__main__':
    # Create a product
    coke_product = Product('Coke')
    coke_product.set_price(8)
    print(f"Created product: {coke_product.get_name()} priced at R${coke_product.get_price()}")

    # Create a vending machine
    vending_machine = VendingMachine('Library')
    vending_machine.add_stock(coke_product, 5)
    print(f"Stock of {coke_product.get_name()} in {vending_machine.get_location()}: {vending_machine.get_stock(coke_product)}")

    # Purchase from vending machine
    print(f"Simulated purchase of 1 {coke_product.get_name()} from {vending_machine.get_location()}: cost R${vending_machine.simulate_purchase(coke_product, 1)}\n")


    # Create another product
    brownie_product = Product('Brownie')
    brownie_product.set_price(15)
    print(f"Created product: {brownie_product.get_name()} priced at R${brownie_product.get_price()}")

    # Create a student vending machine
    student_vending = StudentVending('Student Center', '1234')
    student_vending.set_product(brownie_product)
    student_vending.add_stock(brownie_product, 5)
    print(f"Stock of {brownie_product.get_name()} in {student_vending.get_location()}: {student_vending.get_stock(brownie_product)}")

    # Purchase from student vending machine
    print(f"Purchase from {student_vending.get_location()} of 2 {brownie_product.get_name()}: cost R${student_vending.simulate_purchase(brownie_product, 2)}\n")


    # Try to purchase more than available
    try:
        print(f"Purchase from {student_vending.get_location()} of 10 {brownie_product.get_name()}: cost R${student_vending.simulate_purchase(brownie_product, 10)}")
    except Exception as e:
        print(f"Error: {e}")

    # Try to purchase coke from student vending machine
    try:
        print(f"Purchase from {student_vending.get_location()} of 2 {coke_product.get_name()}: cost R${student_vending.simulate_purchase(coke_product, 2)}")
    except Exception as e:
        print(f"Error: {e}")