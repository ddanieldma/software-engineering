import sys
import os

# Importando module com caminho relativo
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Preciso receber uma lista de produtos e exibir essa lista de uma forma organizada no site.
# Vou criar uma lista com 3 produtos e colocá-los em uma estrutura bem simples no site com flexbox.

from vending import Product

# Creating produtcs.
coke_product = Product('Coke')
coke_product.set_price(8)
brownie_product = Product('Brownie')
brownie_product.set_price(5)
coffee_product = Product('Coffee')
coffee_product.set_price(2)

# Putting in a list.
products_list = [
    coke_product,
    brownie_product,
    coffee_product,
]

for product in products_list:
    print(f"Product name: {product.get_name()}, product price: {product.get_price()}")