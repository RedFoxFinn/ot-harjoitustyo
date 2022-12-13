import unittest
import os
import sqlite3
from tools.db_validator import validate_database_path
from tools.db_validator import validate_database_existence

test_db_paths = ["src/tests/test_db.db",
                 "src/services/test_db.db"]


class Test_validate_database_path(unittest.TestCase):
    def test_path_is_invalid(self):
        resp = validate_database_path(test_db_paths[0])
        self.assertEqual(type(resp), bool)
        self.assertEqual(resp, False)

    def test_path_is_valid(self):
        resp = validate_database_path(test_db_paths[1])
        self.assertEqual(type(resp), bool)
        self.assertEqual(resp, True)


class Test_validate_database_existence(unittest.TestCase):
    def _remove_db_file(self):
        if os.path.isfile(test_db_paths[0]):
            os.remove(test_db_paths[0])
        if os.path.isfile(test_db_paths[1]):
            os.remove(test_db_paths[1])

    def _connect_db_file(self, db_path=test_db_paths[1]):
        sqlite3.connect(db_path)

    def test_nonexistent(self):
        self._remove_db_file()
        resp = validate_database_existence(test_db_paths[1])
        self.assertEqual(type(resp), bool)
        self.assertEqual(resp, False)

    def test_existent(self):
        self._remove_db_file()
        self._connect_db_file()
        resp = validate_database_existence(test_db_paths[1])
        self.assertEqual(type(resp), bool)
        self.assertEqual(resp, True)
