from unittest import TestCase
from Euchre15 import run


class TestGameRunner(TestCase):

    def test_run(self):
        result = run(num_games=1)
        self.assertIn('game wins = 1', result)
