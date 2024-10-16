from abc import ABC, abstractmethod
import vending as v

# Custom exception for permission handling errors
class PermissionError(Exception):
    """Exception raised when a seller tries to perform unauthorized actions."""
    pass


# Person abstract class
class Person(ABC):
    """
    Abstract class representing a person with common attributes like name, email, and password.

    Attributes:
        _name (str): The name of the person.
        _email (str): The email of the person.
        _password (str): The password of the person.

    Methods:
        get_role(): Abstract method to get the role of the person.
    """
    def __init__(self, name, email, password):
        """
        Initializes a Person with a name, email, and password.

        Args:
            name (str): The name of the person.
            email (str): The email of the person.
            password (str): The password of the person.
        """
        self._name = name
        self._email = email
        self._password = password

    @abstractmethod
    def get_role(self):
        """
        Abstract method to get the role of the person.

        Returns:
            str: The role of the person (e.g., 'user', 'admin', or 'seller').
        """
        pass


# User class
class User(Person):
    """
    Class representing a general user in the vending system.

    Inherits from Person.

    Attributes:
        _user_id (int): The unique identifier of the user.

    Methods:
        get_role(): Get the role of the user.
        simulate_purchase(vending_place, product, quantity): Simulate the purchase of a product from a vending place.
    """
    def __init__(self, name, email, password, user_id):
        """
        Initializes a User with a user ID in addition to the Person attributes.

        Args:
            name (str): The name of the user.
            email (str): The email of the user.
            password (str): The password of the user.
            user_id (int): The unique identifier of the user.
        """
        super().__init__(name, email, password)
        self._user_id = user_id

    def get_role(self):
        """
        Get the role of the user.

        Returns:
            str: Returns 'user' as the role.
        """
        return 'user'
    
    def simulate_purchase(self, vending_place, product, quantity):
        """
        Simulates the purchase of a product from a vending place.

        Args:
            vending_place (VendingPlace): The vending place where the purchase is made.
            product (Product): The product being purchased.
            quantity (int): The quantity of the product being purchased.

        Returns:
            float: The total cost of the purchase.

        Raises:
            ValueError: If the vending place is not a valid instance of VendingPlace.
        """
        if not isinstance(vending_place, v.VendingPlace):
            raise ValueError("Invalid vending place")
        
        return vending_place.simulate_purchase(product, quantity)


# Admin class
class Admin(Person):
    """
    Class representing an admin in the vending system who can manage vending machines.

    Inherits from Person.

    Methods:
        get_role(): Get the role of the admin.
        add_product_stock(vending_machine, product, quantity): Add stock to a vending machine.
        remove_product_stock(vending_machine, product, quantity): Remove stock from a vending machine.
    """
    def __init__(self, name, email, password):
        """
        Initializes an Admin with the Person attributes.

        Args:
            name (str): The name of the admin.
            email (str): The email of the admin.
            password (str): The password of the admin.
        """
        super().__init__(name, email, password)

    def get_role(self):
        """
        Get the role of the admin.

        Returns:
            str: Returns 'admin' as the role.
        """
        return 'admin'
    
    def add_product_stock(self, vending_machine, product, quantity):
        """
        Adds stock of a product to a vending machine.

        Args:
            vending_machine (VendingMachine): The vending machine where stock is being added.
            product (Product): The product being stocked.
            quantity (int): The quantity of the product to be added.

        Raises:
            ValueError: If the vending machine is not a valid instance of VendingMachine.
        """
        if not isinstance(vending_machine, v.VendingMachine):
            raise ValueError("Invalid vending machine")

        vending_machine.add_stock(product, quantity)


# Seller class (inherits from User)
class Seller(User):
    """
    Class representing a seller in the vending system, a specialized type of user.
    Sellers are responsible for managing stock in their own vending machine.

    Inherits from User.

    Methods:
        get_role(): Get the role of the seller.
        add_product_stock(student_vending, product, quantity): Add stock to the seller's vending machine.
    """
    def __init__(self, name, email, password, user_id):
        """
        Initializes a Seller with the User attributes.

        Args:
            name (str): The name of the seller.
            email (str): The email of the seller.
            password (str): The password of the seller.
            user_id (int): The unique identifier of the seller.
        """
        super().__init__(name, email, password, user_id)

    def get_role(self):
        """
        Get the role of the seller.

        Returns:
            str: Returns 'seller' as the role.
        """
        return 'seller'
    
    def add_product_stock(self, student_vending, product, quantity):
        """
        Adds product stock to the seller's own vending machine.

        Args:
            student_vending (StudentVending): The student vending machine where stock is being added.
            product (Product): The product being stocked.
            quantity (int): The quantity of the product to be added.

        Raises:
            ValueError: If the vending machine is not a valid instance of StudentVending.
            PermissionError: If the seller is not authorized to add stock to the vending machine.
        """
        if not isinstance(student_vending, v.StudentVending):
            raise ValueError("The vending machine must be a StudentVending instance")
        
        if student_vending.get_student_id() != self._user_id:
            raise PermissionError("Seller is not authorized to add stock to this vending machine")

        student_vending.add_stock(product, quantity)


if __name__ == '__main__':
    # Create a product
    product = v.Product('Soda')
    product.set_price(1.50)
    print(f"Created product: {product.get_name()} priced at R${product.get_price()}")

    # Create a vending machine
    vending_machine = v.VendingMachine('University')

    # Create an admin user
    admin = Admin("John", "john@email.com", "admin")

    # Create a regular user
    user1 = User("Alice", "alice@email.com", "1234", 1)

    # Create a seller user
    seller = Seller("Bob", "bob@email.com", "123123", 2)

    # Admin adds stock to vending machine
    admin.add_product_stock(vending_machine, product, 10)
    print(f"Stock of {product.get_name()} in {vending_machine.get_location()}: {vending_machine.get_stock(product)}")

    # User simulates a purchase
    print(f"Simulated purchase of 1 {product.get_name()} from {vending_machine.get_location()}: cost R${user1.simulate_purchase(vending_machine, product, 1)}\n")

    # Create another product
    product1 = v.Product('Chips')
    product1.set_price(2.50)
    print(f"Created product: {product1.get_name()} priced at R${product1.get_price()}")

    # Create a student vending machine
    student_vending = v.StudentVending('Student Center', 2)
    student_vending.set_product(product1)

    # Seller adds stock to their own student vending machine
    seller.add_product_stock(student_vending, product1, 5)
    print(f"Stock of {product1.get_name()} in {student_vending.get_location()}: {student_vending.get_stock(product1)}")

    # User simulates purchase from student vending machine
    print(f"Purchase from {student_vending.get_location()} of 2 {product1.get_name()}: cost R${user1.simulate_purchase(student_vending, product1, 2)}\n")

    # Try to add a product not sold by the student vending
    try:
        seller.add_product_stock(student_vending, product, 5)
    except Exception as e:
        print(f"Error: {e}")

    # Try to add stock to a regular vending machine (not allowed for seller)
    try:
        seller.add_product_stock(vending_machine, product, 5)
    except Exception as e:
        print(f"Error: {e}")