"""Class Trickset."""
from utils import group_players_as_teams


class Trickset(object):
    """Represents a single deal of the cards; a round."""

    def __init__(self, players, dealer, deck):
        self.players = players
        self.dealer = dealer
        self.deck = deck
        self.team1, self.team2 = group_players_as_teams(self.players)
        self.scores = {
            self.team1: 0,
            self.team2: 0
        }
