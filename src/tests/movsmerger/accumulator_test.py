import datetime
import unittest

from movs.model import Row
from movsmerger import accumulator


def d(days: int=0) -> datetime.date:
    return datetime.date(2020, 1, 1) + datetime.timedelta(days=days)


ROW0 = Row(d(0), d(0), None, None, '')
ROW1 = Row(d(1), d(1), None, None, '')


class AccumulatorTest(unittest.TestCase):

    def test_accumulate_empty_empty(self) -> None:
        self.assertEqual([], accumulator.accumulate([], []))

    def test_accumulate_empty_full(self) -> None:
        self.assertEqual([ROW0], accumulator.accumulate([], [ROW0]))

    def test_accumulate_full_full_equals(self) -> None:
        self.assertEqual([ROW0], accumulator.accumulate([ROW0], [ROW0]))

    def test_accumulate_full_full_new_data(self) -> None:
        self.assertEqual([ROW1, ROW0], accumulator.accumulate([ROW0], [ROW1]))
