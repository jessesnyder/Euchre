"""Class Session."""
from collections import namedtuple
from game import Game
from utils import group_players_as_teams


SessionResult = namedtuple("SessionResult", "winner scores")


class Session(object):
    """Manages the lifetime of a playing session of 1 or
       more games by the same players on the same teams.

       - Keeps track of how many games each team has won.
       - Provides factory methods for generating robot players
         and new Games.
    """

    def __init__(self, players):
        """Players should be passed in the order seated"""
        self.players = players
        self.team1, self.team2 = group_players_as_teams(self.players)
        self.gamescores = {
            self.team1: 0,
            self.team2: 0
        }

    def update_results(self, game_result):
        """Add to the winning team's total."""
        winner = max(game_result.scores, key=game_result.scores.get)
        self.gamescores[winner] += 1

    def new_game(self):
        """Factory for games using these players/teams"""
        return Game(players=self.players)

    @property
    def result(self):
        winner = max(self.gamescores, key=self.gamescores.get)
        return SessionResult(winner=winner, scores=self.gamescores.copy())
