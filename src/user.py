from abc import ABC, abstractmethod
import vending as v


# Custom exception for better error handling
class PermissionError(Exception):
    pass


# Person abstract class
class Person(ABC):
    def __init__(self, name, email, password):
        self._name = name
        self._email = email
        self._password = password

    @abstractmethod
    def get_role(self):
        """Must return the role of the person"""
        pass


# User class
class User(Person):
    def __init__(self, name, email, password, user_id):
        super().__init__(name, email, password)
        self._user_id = user_id

    def get_role(self):
        return 'user'
    
    def simulate_purchase(self, vending_place, product, quantity):
        """Simulate a purchase of a product from a vending place"""
        if not isinstance(vending_place, v.VendingPlace):
            raise ValueError("Invalid vending place")
        
        return vending_place.simulate_purchase(product, quantity)

# Admin class
class Admin(Person):
    def __init__(self, name, email, password):
        super().__init__(name, email, password)

    def get_role(self):
        return 'admin'
    
    def add_product_stock(self, vending_machine, product, quantity):
        """Add stock of a product to a vending machine"""
        if not isinstance(vending_machine, v.VendingMachine):
            raise ValueError("Invalid vending machine")

        vending_machine.add_stock(product, quantity)

# Seller class (inherits from User)
class Seller(User):
    def __init__(self, name, email, password, user_id):
        super().__init__(name, email, password, user_id)

    def get_role(self):
        return 'seller'
    
    def add_product_stock(self, student_vending, product, quantity):
        """Allows the seller to add product stock to their own vending machine"""
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

    # Create a admin user
    admin = Admin("John", "john@email.com", "admin")

    # Create a user
    user1 = User("Alice", "alice@email.com", "1234", 1)

    # Create a seller user
    seller = Seller("Bob", "bob@email.com", "123123", 2)

    # Admin adds stock to vending machine
    admin.add_product_stock(vending_machine, product, 10)
    print(f"Stock of {product.get_name()} in {vending_machine.get_location()}: {vending_machine.get_stock(product)}")

    # User simulates purchase
    print(f"Simulated purchase of 1 {product.get_name()} from {vending_machine.get_location()}: cost R${user1.simulate_purchase(vending_machine, product, 1)}\n")

    # Create another product
    product1 = v.Product('Chips')
    product1.set_price(2.50)
    print(f"Created product: {product1.get_name()} priced at R${product1.get_price()}")

    # Create a student vending machine
    student_vending = v.StudentVending('Student Center', 2)
    student_vending.set_product(product1)

    # Seller adds stock to student vending machine
    seller.add_product_stock(student_vending, product1, 5)
    print(f"Stock of {product1.get_name()} in {student_vending.get_location()}: {student_vending.get_stock(product1)}")

    # User simulates purchase from student vending machine
    print(f"Purchase from {student_vending.get_location()} of 2 {product1.get_name()}: cost R${user1.simulate_purchase(student_vending, product1, 2)}\n")

    # Try to add wrong product to student vending
    try:
        seller.add_product_stock(student_vending, product, 5)
    except Exception as e:
        print(f"Error: {e}")

    # Try to add stock to vending machine directly
    try:
        seller.add_product_stock(vending_machine, product, 5)
    except Exception as e:
        print(f"Error: {e}")