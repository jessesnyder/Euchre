"""Class Game."""
from collections import namedtuple
import random
from trickset import Trickset
from utils import group_players_as_teams
from utils import next_in_rotation


BOT_PLAYER_NAMES = ['Sam', 'Kim', 'Sue', 'Tim']


GameResult = namedtuple("GameResult", "scores")


class Game(object):
    """State and actions for a game."""

    POINTS_TO_WIN = 10
    _cards_per_hand = 5

    def __init__(self, players):
        self.players = players
        self.team1, self.team2 = group_players_as_teams(self.players)
        self.scores = {
            self.team1: 0,
            self.team2: 0
        }
        self.current_dealer = None
        self.current_winner = None
        self.set_new_dealer()

    @property
    def over(self):
        return max(self.scores.values()) >= self.POINTS_TO_WIN

    def new_trickset(self):
        """Factory for Tricksets, which are played until the game score
           or one team is high enough to win the game.
        """
        self.set_new_dealer()
        return Trickset(players=self.players, dealer=self.current_dealer)

    def update_results(self, result):
        """Update the game score based on a Trickset (a round or deal)."""
        for team in (self.team1, self.team2):
            self.scores[team] += result.scores[team]

    def result(self):
        """Return the result of a completed game."""
        if not self.over:
            raise Exception("Game is not over!")

        return GameResult(scores=self.scores.copy())

    def set_new_dealer(self):
        if self.current_dealer is None:
            self.current_dealer = random.choice(self.players)
        else:
            current_index = self.players.index(self.current_dealer)
            self.current_dealer = next_in_rotation(self.players, current_index)
        self.current_dealer.isDealer = True
