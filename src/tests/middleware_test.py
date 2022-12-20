
import os
import unittest
from services.middleware import Middleware
from services.db_handler import DatabaseHandler
from tools.date_tools import get_current_date
from tools.date_tools import get_exp_timestamp

test_db_path = "src/services/test_db.db"

test_db_products = [
    ['Goatly deluxe', 1, 1649531257, 0, 4],
    ['Soijakastike', 3, 1649531257, 12, 1],
    ['Maitosuklaa 200g', 2, 1649531257, 0, 8],
    ['Taloussuklaa 200g', 2, 1649531257, 0, 5],
    ['Appelsiini', 3, 1681067257, 1, 7],
    ['Tattarijauho', 3, 1681067257, 20, 2]
]

test_product_for_add = {
    'name': 'OddlyGoo veggie slice',
    'type': 2,
    'exp': 1281067257,
    'subtype': 0,
    'count': 2
}


class Test_Middleware(unittest.TestCase):
    def setUp(self):
        if os.path.isfile('src/services/test_db.db'):
            os.remove('src/services/test_db.db')
        self._dbh = DatabaseHandler(False, test_db_path)
        self._mw = Middleware(self._dbh)

        for product in test_db_products:
            self._mw.add_product(pname=product[0], ptype=product[1],
                                 pexp=product[2], psubtype=product[3], pcount=product[4])

    def test_middleware_existent(self):
        self.assertEqual(type(self._mw), Middleware)

    def test_middleware_get_types(self):
        result = self._mw.get_types()
        self.assertEqual(len(result), 3)

    def test_middleware_get_numbers_by_types(self):
        result = self._mw.get_numbers_by_types()
        self.assertEqual(type(result[0][0]), int)
        self.assertEqual(result[0][0], 1)
        self.assertEqual(type(result[0][2]), int)
        self.assertEqual(result[0][2], 4)
        self.assertEqual(type(result[1][0]), int)
        self.assertEqual(result[1][0], 2)
        self.assertEqual(type(result[1][2]), int)
        self.assertEqual(result[1][2], 13)
        self.assertEqual(type(result[2][0]), int)
        self.assertEqual(result[2][0], 3)
        self.assertEqual(type(result[2][2]), int)
        self.assertEqual(result[2][2], 10)

    def test_middleware_get_products(self):
        result = self._mw.get_products()
        self.assertEqual(len(result), 6)
        self.assertEqual(result[2], (2, 'Soijakastike', 1649531257,
                         1, 'Raaka-aineet', 12, 'Maustekastikkeet'))

    def test_middleware_get_product_count(self):
        result = self._mw.get_product_count()
        self.assertEqual(type(result), int)
        self.assertEqual(result, 6)

    def test_middleware_get_expiring_products(self):
        exp = get_exp_timestamp(year=2023, month=6, day=1)
        result = self._mw.get_expiring_products(timestamp=exp)
        self.assertEqual(len(result), 2)
        self.assertEqual(result[0][0], 7)

    def test_middleware_get_expiring_products_count(self):
        exp = get_exp_timestamp(year=2023, month=6, day=1)
        result = self._mw.get_expiring_products_count(timestamp=exp)
        self.assertEqual(type(result), int)
        self.assertEqual(result, 9)

    def test_middleware_get_expired_products(self):
        exp = get_current_date()
        result = self._mw.get_expired_products(timestamp=exp)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0][0], 4)

    def test_middleware_get_expired_products_count(self):
        exp = get_current_date()
        result = self._mw.get_expired_products_count(timestamp=exp)
        self.assertEqual(type(result), int)
        self.assertEqual(result, 18)

    def test_middleware_get_types_for_selector(self):
        result = self._mw.get_types_for_selector()
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[0], f"{0:02d} - valitse tyyppi")

    def test_middleware_get_subtypes_for_selector(self):
        result = self._mw.get_subtypes_for_selector()
        self.assertEqual(type(result), list)
        self.assertEqual(len(result), 21)
        self.assertEqual(result[0], f"{0:02d} - valitse alatyyppi")

    def test_middleware_x_add_product(self):
        result = self._mw.add_product(
            pname=test_product_for_add['name'],
            ptype=test_product_for_add['type'],
            pexp=test_product_for_add['exp'],
            psubtype=test_product_for_add['subtype'],
            pcount=test_product_for_add['count']
        )
        self.assertEqual(type(result), bool)
        self.assertEqual(result, True)

    def test_middleware_x_update_product_add(self):
        self._mw.add_product(
            pname=test_product_for_add['name'],
            ptype=test_product_for_add['type'],
            pexp=test_product_for_add['exp'],
            psubtype=test_product_for_add['subtype'],
            pcount=test_product_for_add['count']
        )
        result = self._mw.update_product(pid=7, change=2, subtract=False)
        self.assertEqual(type(result), bool)
        self.assertEqual(result, True)
        products = self._mw.get_products()
        test_product = [elem for elem in products if elem[0] == 7]
        self.assertEqual(len(test_product), 1)
        self.assertEqual(test_product[0][3], test_product_for_add['count']+2)

    def test_middleware_x_update_product_subtract(self):
        self._mw.add_product(
            pname=test_product_for_add['name'],
            ptype=test_product_for_add['type'],
            pexp=test_product_for_add['exp'],
            psubtype=test_product_for_add['subtype'],
            pcount=test_product_for_add['count']
        )
        result = self._mw.update_product(pid=7, change=1, subtract=True)
        self.assertEqual(type(result), bool)
        self.assertEqual(result, True)
        products = self._mw.get_products()
        test_product = [elem for elem in products if elem[0] == 7]
        self.assertEqual(len(test_product), 1)
        self.assertEqual(test_product[0][3], test_product_for_add['count']-1)

    def test_middleware_x_update_product_remove(self):
        self._mw.add_product(
            pname=test_product_for_add['name'],
            ptype=test_product_for_add['type'],
            pexp=test_product_for_add['exp'],
            psubtype=test_product_for_add['subtype'],
            pcount=test_product_for_add['count']
        )
        result = self._mw.update_product(pid=7, remove=True)
        self.assertEqual(type(result), bool)
        self.assertEqual(result, True)
        products = self._mw.get_products()
        test_product = [elem for elem in products if elem[0] == 7]
        self.assertEqual(len(test_product), 0)
