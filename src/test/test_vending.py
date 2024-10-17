import os 
import sys

sys.path.append(os.path.join(os.path.dirname(__file__), '..'))

import unittest

from vending import get_products_from_db, Product

class TestProductDatabase(unittest.TestCase):
    def test_get_products_from_db(self):
        products = get_products_from_db()
        self.assertIsInstance(products, list)
        self.assertEqual(len(products), 0)

if __name__ == '__main__':
    unittest.main()
