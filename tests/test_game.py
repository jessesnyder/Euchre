from unittest import TestCase
from player import Player
from game import Game


class TestGame(TestCase):

    def _make_one(self):
        players = (
            Player("Amy"), Player("Bonnie"), Player("Andy"), Player("Bill")
        )

        return Game(players=players)

    def test_scores_zero_before_first_round(self):
        game = self._make_one()
        self.assertEqual(0, game.scores[game.team1])
        self.assertEqual(0, game.scores[game.team2])

    def test_update_results_adds_trickset_scores(self):
        game = self._make_one()
        round1 = game.new_trickset()
        round1.scores[game.team1] = 2
        game.update_results(round1)
        self.assertEqual(2, game.scores[game.team1])
        self.assertEqual(0, game.scores[game.team2])

    def test_new_trickset_dealer_is_some_player(self):
        game = self._make_one()
        round1 = game.new_trickset()
        self.assertIn(round1.dealer, game.players)

    def test_dealer_rotates_by_round(self):
        game = self._make_one()
        round1 = game.new_trickset()
        round2 = game.new_trickset()
        self.assertNotEqual(round1.dealer, round2.dealer)
