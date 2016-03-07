"""Class Trickset."""
from utils import group_players_as_teams
from deck import Deck
from deck import SUITS


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
    def deal(self):
        self.deck = Deck()
        for i in range(self.CARDS_PER_HAND):
            for p in self.players:
                p.add_card(self.deck.pop())


    @property
    def bidders_in_order(self):
        """Start with the next in line from the dealer"""
        leader_index = self.players.index(self.dealer) + 1
        return self.players[leader_index:] + self.players[:leader_index]

    def run_bidding_round_1(self):
        """ Return an actual bid or None """
        return self._run_bidding_round('bid_first_round')

    def run_bidding_round_2(self):
        """ Run bidding in suits of player's choice, if everyone passed
            in round 1
        """
        return self._run_bidding_round('bid_second_round')

    def _run_bidding_round(self, bid_method):
        topcard = self.deck[0]
        for position, bidmaker in enumerate(self.bidders_in_order):
            method = getattr(bidmaker, bid_method)
            bid = method(
                player_position=position,
                topcard=topcard
            )
            if not bid.is_pass:
                return bid

        return None
