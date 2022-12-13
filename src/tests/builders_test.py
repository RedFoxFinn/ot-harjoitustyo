
import unittest

from tools.builders import build_elements_for_selector
from tools.builders import build_id_from_selector_number

types = [
    ('Juomat', 1),
    ('Ruoat', 2),
    ('Raaka-aineet', 3)]

subtypes = [
    ('Raaka-aineet', 'Hedelmät', 1),
    ('Raaka-aineet', 'Juomajauheet', 2),
    ('Raaka-aineet', 'Juomatiivisteet', 3),
    ('Raaka-aineet', 'Kalat', 4),
    ('Raaka-aineet', 'Kasvikset', 5),
    ('Raaka-aineet', 'Kasvipohjaiset valmisteet', 6),
    ('Raaka-aineet', 'Leivonta', 7),
    ('Raaka-aineet', 'Lihat', 8),
    ('Raaka-aineet', 'Maitotuotteet', 9),
    ('Raaka-aineet', 'Marjat', 10),
    ('Raaka-aineet', 'Mausteet', 11),
    ('Raaka-aineet', 'Maustekastikkeet', 12),
    ('Raaka-aineet', 'Munat', 13),
    ('Raaka-aineet', 'Puolivalmisteet', 14),
    ('Raaka-aineet', 'Rasvat, öljyt', 15),
    ('Raaka-aineet', 'Ravintojauheet', 16),
    ('Raaka-aineet', 'Sokerit', 17),
    ('Raaka-aineet', 'Säilykkeet', 18),
    ('Raaka-aineet', 'Vihannekset', 19),
    ('Raaka-aineet', 'Viljatuotteet', 20)]


class Test_builders(unittest.TestCase):
    def test_build_elements_for_selector_empty_list_type(self):
        result = build_elements_for_selector()
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], f"{0:02d} - valitse tyyppi")

    def test_build_elements_for_selector_empty_list_subtype(self):
        result = build_elements_for_selector(for_type=False)
        self.assertEqual(len(result), 1)
        self.assertEqual(result[0], f"{0:02d} - valitse alatyyppi")

    def test_build_elements_for_selector_type(self):
        result = build_elements_for_selector(list_of=types)
        self.assertEqual(len(result), 4)
        self.assertEqual(result[1], f"{1:02d} - Juomat")

    def test_build_elements_for_selector_subtype(self):
        result = build_elements_for_selector(list_of=subtypes, for_type=False)
        self.assertEqual(len(result), 21)
        self.assertEqual(result[10], f"{10:02d} - Marjat")

    def test_build_id_from_selector_number_zero_prefix(self):
        result = build_id_from_selector_number(selector_number_str="02")
        self.assertEqual(result, 2)

    def test_build_id_from_selector_number_no_prefix(self):
        result = build_id_from_selector_number(selector_number_str="17")
        self.assertEqual(result, 17)
