from collections import defaultdict

# Product class
class Product:
    def __init__(self, name):
        self._name = name
        self._price = None

    def set_price(self, price):
        if not isinstance(price, (int, float)):
            raise ValueError('Price must be a number')
        elif price <= 0:
            raise ValueError('Price must be positive')
        
        self._price = price

    def get_price(self):
        if self._price is None:
            raise ValueError('Price is not set')
        
        return self._price
    
    def get_name(self):
        return self._name


# Vending place superclass
class VendingPlace:
    def __init__(self, location):
        self._location = location

    def get_location(self):
        return self._location
    
    def get_stock(self):
        pass

    def set_stock(self):
        pass

    def add_stock(self, product, quantity):
        if not isinstance(product, Product):
            raise ValueError('Product must be a Product instance')
        elif not isinstance(quantity, int):
            raise ValueError('Quantity must be an integer')
        elif quantity <= 0:
            raise ValueError('Quantity must be positive')

        new_quantity = self.get_stock(product) + quantity
        self.set_stock(product, new_quantity)

    def simulate_purchase(self, product, quantity):
        if not isinstance(product, Product):
            raise ValueError('Product must be a Product instance')
        elif not isinstance(quantity, int):
            raise ValueError('Quantity must be an integer')
        elif quantity <= 0:
            raise ValueError('Quantity must be positive')

        if self.get_stock(product) < quantity:
            raise ValueError(f'Not enough stock! {quantity} requested but only {self.get_stock(product)} available')
        
        return product.get_price() * quantity


# Vending machine class
class VendingMachine(VendingPlace):
    def __init__(self, location):
        super().__init__(location)
        self._stock = defaultdict(int)

    def get_stock(self, product):
        if not isinstance(product, Product):
            raise ValueError('Product must be a Product instance')

        return self._stock[product]
    
    def set_stock(self, product, quantity):
        if not isinstance(product, Product):
            raise ValueError('Product must be a Product instance')
        elif not isinstance(quantity, int):
            raise ValueError('Quantity must be an integer')
        elif quantity < 0:
            raise ValueError('Quantity must be non-negative')

        self._stock[product] = quantity


# Student vending class
class StudentVending(VendingMachine):
    def __init__(self, location, student_id):
        super().__init__(location)
        self._student_id = student_id
        self._product = None
        self._stock = 0

    def get_student_id(self):
        return self._student_id
    
    def set_product(self, product):
        if not isinstance(product, Product):
            raise ValueError('Product must be a Product instance')

        self._product = product

    def get_product(self):
        return self._product
    
    def set_stock(self, product, quantity):
        if product != self._product:
            raise ValueError('This student does not sell this product')
        
        self._stock = quantity
    
    def get_stock(self, product):
        if product != self._product:
            raise ValueError('This student does not sell this product')
        
        return self._stock


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


    # Create a artesenal product
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
    except ValueError as e:
        print(e)

    # Try to purchase coke from student vending machine
    try:
        print(f"Purchase from {student_vending.get_location()} of 2 {coke_product.get_name()}: cost R${student_vending.simulate_purchase(coke_product, 2)}")
    except ValueError as e:
        print(e)