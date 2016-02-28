"""Class Session."""
from deck import Deck
from game import Game
from utils import group_players_as_teams


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
        self._set_partners(self.team1)
        self._set_partners(self.team2)

    def increment_game_scores(self, game):
        """Add to the winning team's total."""
        winner = max(game.scores, key=game.scores.get)
        self.gamescores[winner] += 1

    def new_game(self):
        """Factory for games using these players/teams"""
        return Game(players=self.players, deck=Deck())

    def _set_partners(self, team):
        team[0].setpartner(team[1])
        team[1].setpartner(team[0])
