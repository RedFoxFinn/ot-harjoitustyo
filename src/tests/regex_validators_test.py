
import unittest
from tools.regex_validators import selector_type_validation_for_ingredient

types = [
    "01 - Juomat",
    "02 - Ruoat",
    "03 - Raaka-aineet"]


class Test_regex_validators(unittest.TestCase):
    def test_selector_type_validation_for_not_ingredient(self):
        result = selector_type_validation_for_ingredient(types[1])
        self.assertEqual(result, False)

    def test_selector_type_validation_for_ingredient(self):
        result = selector_type_validation_for_ingredient(types[2])
        self.assertEqual(result, True)
