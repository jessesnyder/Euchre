from unittest import TestCase
from player import Player
from session import Session


class TestSession(TestCase):

    def test_new_session_organizes_teams(self):
        players = (
            Player("Amy"), Player("Bonnie"), Player("Andy"), Player("Bill")
        )
        Session(players=players)

        self.assertEqual(players[0].partner, players[2])

    def test_game_scores_zero_before_play(self):
        players = (
            Player("Amy"), Player("Bonnie"), Player("Andy"), Player("Bill")
        )
        session = Session(players=players)

        self.assertEqual(session.gamescores[session.team1], 0)
        self.assertEqual(session.gamescores[session.team2], 0)

    def test_update_game_score(self):
        players = (
            Player("Amy"), Player("Bonnie"), Player("Andy"), Player("Bill")
        )
        session = Session(players=players)
        game = session.new_game()
        game.scores[session.team1] = 10
        game.scores[session.team2] = 8

        session.increment_game_scores(game)

        self.assertEqual(session.gamescores[session.team1], 1)
        self.assertEqual(session.gamescores[session.team2], 0)
