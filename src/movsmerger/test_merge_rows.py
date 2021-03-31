from datetime import date
from datetime import timedelta
from unittest import TestCase

from movs.model import Row

from . import merge_rows


def d(days: int = 0) -> date:
    return date(2020, 1, 1) + timedelta(days=days)


ROW0 = Row(d(0), d(0), None, None, '')
ROW1 = Row(d(1), d(1), None, None, '')


class MergeRowsTest(TestCase):

    def test_empty_empty(self) -> None:
        self.assertListEqual([], list(merge_rows([], [])))

    def test_empty_full(self) -> None:
        self.assertListEqual([ROW0], list(merge_rows([], [ROW0])))

    def test_full_full_equals(self) -> None:
        self.assertListEqual([ROW0], list(merge_rows([ROW0], [ROW0])))

    def test_full_full_new_data(self) -> None:
        self.assertListEqual([ROW1, ROW0], list(merge_rows([ROW0], [ROW1])))
