"""Class Trickset."""


class Trickset(object):
    """Represents a single deal of the cards; a round."""

    def __init__(self, players, dealer, deck):
        self.players = players
        self.dealer = dealer
        self.deck = deck
