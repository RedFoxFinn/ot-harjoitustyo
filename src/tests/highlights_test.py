
import unittest
import datetime
from tools.highlights import highlight_expired_label


class Test_highlights(unittest.TestCase):
    def test_highlight_expiring(self):
        expiring_date = datetime.date.today() + datetime.timedelta(days=1)
        expiring_date_timestamp = datetime.datetime(
            expiring_date.year, expiring_date.month, expiring_date.day).timestamp()
        result = highlight_expired_label(expiring_date_timestamp)
        self.assertEqual(result, "orange")

    def test_highlight_expired(self):
        expired_date = datetime.date.today() + datetime.timedelta(days=-1)
        expired_date_timestamp = datetime.datetime(
            expired_date.year, expired_date.month, expired_date.day).timestamp()
        result = highlight_expired_label(expired_date_timestamp)
        self.assertEqual(result, "red")

    def test_highlight_valid(self):
        valid_date = datetime.date.today() + datetime.timedelta(days=10)
        valid_date_timestamp = datetime.datetime(
            valid_date.year, valid_date.month, valid_date.day).timestamp()
        result = highlight_expired_label(valid_date_timestamp)
        self.assertEqual(result, "black")
