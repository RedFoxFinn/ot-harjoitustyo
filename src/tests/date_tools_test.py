import unittest
import datetime

from tools.date_tools import get_current_date
from tools.date_tools import get_soon_exp_date


class Test_date_tools(unittest.TestCase):
    current_date = datetime.date.today()
    exp_soon_date = current_date + datetime.timedelta(days=5)
    current_timestamp = datetime.datetime(
        current_date.year, current_date.month, current_date.day
    ).timestamp()
    exp_soon_timestamp = datetime.datetime(
        exp_soon_date.year, exp_soon_date.month, exp_soon_date.day
    ).timestamp()

    def test_get_current_date(self):
        stamp = get_current_date()
        self.assertEqual(type(stamp), float)
        self.assertEqual(stamp, self.current_timestamp)

    def test_get_current_date_as_object(self):
        obj = get_current_date(as_object=True)
        self.assertEqual(type(obj), datetime.date)
        self.assertEqual(obj, self.current_date)

    def test_get_soon_exp_date(self):
        stamp = get_soon_exp_date(days_to_add=5)
        self.assertEqual(type(stamp), float)
        self.assertEqual(stamp, self.exp_soon_timestamp)
