import sys
import os

# Importando module com caminho relativo
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Preciso receber uma lista de produtos e exibir essa lista de uma forma organizada no site.
# Vou criar uma lista com 3 produtos e colocá-los em uma estrutura bem simples no site com flexbox.

from vending import Product, VendingMachine

vending_machines_list = [
    VendingMachine("Library"),
    VendingMachine("8th floor"),
    VendingMachine("9th floor")
]

# Creating vending machines.
coke_product = Product('Coke', "", 8, "")
brownie_product = Product('Brownie', "", 5, "")
coffee_product = Product('Coffee', "", 2, "")
soda_product = Product('Soda', "", 7, "")
cookies_product = Product('Cookies', "", 4, "")

products = {
    "Library": [coke_product, brownie_product, coffee_product],
    "8th floor": [coke_product, soda_product, cookies_product],
    "9th floor": [cookies_product, cookies_product]
}