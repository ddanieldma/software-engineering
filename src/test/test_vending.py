import os 
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import unittest

from vending import get_products_from_db, Product

class TestProductDatabase(unittest.TestCase):
    def test_get_empty_product_list(self):
        products = get_products_from_db()
        self.assertIsInstance(products, list)
        self.assertEqual(len(products), 0)

    def test_getting_non_empty_list(self):
        products = get_products_from_db()
        self.assertEqual(len(products), 2)
        self.assertIsInstance(products[0], Product)
        self.assertEqual(products[0].get_name(), "Coke")
        self.assertEqual(products[0].get_price(), 8)

if __name__ == '__main__':
    unittest.main()
