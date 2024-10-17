import sys
import os

# Importando module com caminho relativo
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import vending as v

# Get all vending machines
vending_machines_list = v.DBConnection().get_all_vending_machines()

# Get all products
vending_machines_products = {vm: vm.get_stock() for vm in vending_machines_list}