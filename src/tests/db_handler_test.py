import unittest
import os
from database.db_handler import DatabaseHandler

test_db_paths = ["src/tests/test_db.db",
                 "src/database/pantry.db",
                 "src/database/test_db.db"]

test_db_types = [
    ('Juomat',1),
    ('Ruoat',2),
    ('Raaka-aineet',3)
]

test_db_subtypes = [
    ('Raaka-aineet', 'Hedelmät',1),
    ('Raaka-aineet', 'Juomajauheet',2),
    ('Raaka-aineet', 'Juomatiivisteet',3),
    ('Raaka-aineet', 'Kalat',4),
    ('Raaka-aineet', 'Kasvikset',5),
    ('Raaka-aineet', 'Leivonta',6),
    ('Raaka-aineet', 'Lihat',7),
    ('Raaka-aineet', 'Maitotuotteet',8),
    ('Raaka-aineet', 'Marjat',9),
    ('Raaka-aineet', 'Mausteet',10),
    ('Raaka-aineet', 'Maustekastikkeet',11),
    ('Raaka-aineet', 'Munat',12),
    ('Raaka-aineet', 'Puolivalmisteet',13),
    ('Raaka-aineet', 'Rasvat, öljyt',14),
    ('Raaka-aineet', 'Ravintojauheet',15),
    ('Raaka-aineet', 'Sokerit',16),
    ('Raaka-aineet', 'Säilykkeet',17),
    ('Raaka-aineet', 'Vihannekset',18),
    ('Raaka-aineet', 'Viljatuotteet',19)
]

test_db_products = [
    ['Goatly deluxe', 1, 1671910001],
    (1, 'Goatly deluxe', 1671910001, 1, 'Juomat', 0, None),
    ['Soijakastike', 3, 1671910001, 11],
    (1, 'Soijakastike', 1671910001, 1, 'Raaka-aineet', 11, 'Maustekastikkeet'),
    ['Maitosuklaa 200g', 2, 1671910001, 0, 2],
    (1, 'Maitosuklaa 200g', 1671910001, 2, 'Ruoat', 0, None)
]


class Test_DatabaseHandler(unittest.TestCase):
    __dbh = None

    def _remove_db_files(self):
        if os.path.isfile(test_db_paths[1]):
            os.remove(test_db_paths[1])
        if os.path.isfile(test_db_paths[2]):
            os.remove(test_db_paths[2])

    def test_dbh_does_not_exist(self):
        self._remove_db_files()
        self.assertEqual(self.__dbh, None)

    def test_db_connection_nonexistent(self):
        self.__dbh = DatabaseHandler(False, test_db_paths[2])
        self.assertEqual(type(self.__dbh), DatabaseHandler)
        self.assertEqual(os.path.isfile(test_db_paths[0]), False)
        self.assertEqual(os.path.isfile(test_db_paths[2]), True)

    def test_db_connection_existent_invalid_path(self):
        self.__dbh = DatabaseHandler(True, test_db_paths[0])
        self.assertEqual(type(self.__dbh), DatabaseHandler)
        self.assertEqual(os.path.isfile(test_db_paths[0]), False)
        self.assertEqual(os.path.isfile(test_db_paths[1]), True)

    def test_db_connection_nonexistent_valid_path(self):
        self.__dbh = DatabaseHandler(False, test_db_paths[2])
        self.assertEqual(type(self.__dbh), DatabaseHandler)
        self.assertEqual(os.path.isfile(test_db_paths[2]), True)

    def test_db_connection_existent_valid_path(self):
        self.__dbh = DatabaseHandler(True, test_db_paths[2])
        self.assertEqual(type(self.__dbh), DatabaseHandler)
        self.assertEqual(os.path.isfile(test_db_paths[2]), True)
        self._remove_db_files()

    def test_db_contains_no_products(self):
        self.__dbh = DatabaseHandler(False, test_db_paths[2])
        self.assertEqual(self.__dbh.get_products(), None)
        self.assertEqual(self.__dbh.get_productcount(), 0)
        self._remove_db_files()

    def test_db_contains_types(self):
        self.__dbh = DatabaseHandler(False, test_db_paths[2])
        _types = self.__dbh.get_types()
        self.assertEqual(len(_types), 3)
        self.assertEqual(self.__dbh.get_typecount(), 3)
        for t in test_db_types:
            self.assertIn(t, _types)
        self._remove_db_files()

    def test_db_contains_subtypes(self):
        self.__dbh = DatabaseHandler(False, test_db_paths[2])
        _subtypes = self.__dbh.get_subtypes()
        self.assertEqual(len(_subtypes), 19)
        self.assertEqual(self.__dbh.get_subtypecount(), 19)
        for s in test_db_subtypes:
            self.assertIn(s, _subtypes)
        self._remove_db_files()

    def test_db_adding_product_without_subtype_count(self):
        self._remove_db_files()
        self.__dbh = DatabaseHandler(False, test_db_paths[2])
        resp = self.__dbh.add_product(
            test_db_products[0][0], test_db_products[0][1], test_db_products[0][2])
        self.assertEqual(resp, True)
        _products = self.__dbh.get_products()
        self.assertEqual(len(_products), 1)
        self.assertIn(test_db_products[1], _products)

    def test_db_adding_product_with_subtype(self):
        self._remove_db_files()
        self.__dbh = DatabaseHandler(False, test_db_paths[2])
        resp = self.__dbh.add_product(
            test_db_products[2][0], test_db_products[2][1], test_db_products[2][2], subtype=test_db_products[2][3])
        self.assertEqual(resp, True)
        _products = self.__dbh.get_products()
        self.assertEqual(len(_products), 1)
        self.assertIn(test_db_products[3], _products)
        self._remove_db_files()

    def test_db_adding_product_with_count(self):
        self._remove_db_files()
        self.__dbh = DatabaseHandler(False, test_db_paths[2])
        resp = self.__dbh.add_product(
            test_db_products[4][0], test_db_products[4][1], test_db_products[4][2], count=test_db_products[4][4])
        self.assertEqual(resp, True)
        _products = self.__dbh.get_products()
        self.assertEqual(len(_products), 1)
        self.assertIn(test_db_products[5], _products)

    def test_db_subtract_from_count(self):
        self._remove_db_files()
        self.__dbh = DatabaseHandler(False, test_db_paths[2])
        resp = self.__dbh.add_product(
            test_db_products[4][0], test_db_products[4][1], test_db_products[4][2], count=test_db_products[4][4])
        self.assertEqual(resp, True)
        resp2 = self.__dbh.update_count(1, 1, True)
        self.assertEqual(resp2, True)
        _products = self.__dbh.get_products()
        self.assertEqual(len(_products), 1)
        self.assertEqual(_products[0][3], test_db_products[4][4]-1)

    def test_db_add_to_count(self):
        self._remove_db_files()
        self.__dbh = DatabaseHandler(False, test_db_paths[2])
        resp = self.__dbh.add_product(
            test_db_products[4][0], test_db_products[4][1], test_db_products[4][2], count=test_db_products[4][4])
        self.assertEqual(resp, True)
        resp2 = self.__dbh.update_count(1, 1, False)
        self.assertEqual(resp2, True)
        _products = self.__dbh.get_products()
        self.assertEqual(len(_products), 1)
        self.assertEqual(_products[0][3], test_db_products[4][4]+1)

    def test_db_subtract_as_remove(self):
        self._remove_db_files()
        self.__dbh = DatabaseHandler(False, test_db_paths[2])
        resp = self.__dbh.add_product(
            test_db_products[4][0], test_db_products[4][1], test_db_products[4][2], count=test_db_products[4][4])
        self.assertEqual(resp, True)
        resp2 = self.__dbh.update_count(1, 2, True)
        self.assertEqual(resp2, True)
        _products = self.__dbh.get_products()
        self.assertEqual(_products, None)

    def test_db_remove_product(self):
        self._remove_db_files()
        self.__dbh = DatabaseHandler(False, test_db_paths[2])
        resp = self.__dbh.add_product(
            test_db_products[4][0], test_db_products[4][1], test_db_products[4][2], count=test_db_products[4][4])
        self.assertEqual(resp, True)
        resp2 = self.__dbh.remove_product(1)
        self.assertEqual(resp2, True)
        _products = self.__dbh.get_products()
        self.assertEqual(_products, None)
