"""test_utils.py"""
from unittest import TestCase
from utils import next_in_rotation


class Test_next_in_rotation(TestCase):

    def test_current_index_0_returns_item_at_1(self):
        seq = ('a', 'b', 'c')
        self.assertEqual(
            'b',
            next_in_rotation(sequence=seq, current_index=0)
        )

    def test_current_index_item_returns_item_at_0(self):
        seq = ('a', 'b', 'c')
        self.assertEqual(
            'a',
            next_in_rotation(sequence=seq, current_index=2)
        )
