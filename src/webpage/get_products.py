import sys
import os

# Importando module com caminho relativo
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

# Preciso receber uma lista de produtos e exibir essa lista de uma forma organizada no site.
# Vou criar uma lista com 3 produtos e colocá-los em uma estrutura bem simples no site com flexbox.

import vending as v

# Get all vending machines
vending_machines = v.DBConnection().get_all_vending_machines()

products_dict = {}
for vending_machine in vending_machines:
    products_dict.update(vending_machine.get_stock())

for product, quantity in products_dict.items():
    print(f"Product name: {product}, product price: {quantity}")