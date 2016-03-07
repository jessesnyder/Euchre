"""Class Trickset."""
from collections import namedtuple
from utils import group_players_as_teams
from deck import Deck
from deck import SUITS
from deck import limit_to_suit


TricksetResult = namedtuple("TricksetResult", "scores")


class Trickset(object):
    """Represents a single deal of the cards; a round."""

    CARDS_PER_HAND = 5

    def __init__(self, players, dealer):
        self.players = players
        self.dealer = dealer
        self.deck = None
        self.team1, self.team2 = group_players_as_teams(self.players)
        self.scores = {
            self.team1: 0,
            self.team2: 0
        }
        self.tricks = {
            self.team1: 0,
            self.team2: 0
        }
        self.current_leader = self.bidders_in_order[0]
        self.bid = None
        self.tricksequence = self.bidders_in_order
        self.played_cards = []

    def run(self):
        """Bidding and play. Return scores."""
        while self.bid is None or self.bid.is_pass:
            self.deal()
            self.bid = self.run_bidding_round_1() or self.run_bidding_round_2()
        winner = self.first_trick()
        self._increment_trick_count(winner)
        winner = self.normal_trick(winner)
        self._increment_trick_count(winner)
        winner = self.normal_trick(winner)
        self._increment_trick_count(winner)
        winner = self.normal_trick(winner)
        self._increment_trick_count(winner)
        winner = self.normal_trick(winner)
        self._increment_trick_count(winner)

        self.score_round()

        return TricksetResult(scores=self.scores.copy())

    def deal(self):
        self.deck = Deck()
        for i in range(self.CARDS_PER_HAND):
            for p in self.players:
                p.add_card(self.deck.pop())

    def trick_sequence(self, winner=None):
        active_players = self.bidders_in_order
        if self.bid.is_alone:
            bidders_partner = self.bid.player.partner
            active_players = tuple(
                [p for p in self.bidders_in_order if p is not bidders_partner]
            )
        if winner is None:
            return active_players

        winner_index = active_players.index(winner)
        return active_players[winner_index:] + active_players[:winner_index]

    @property
    def leader(self):
        return self.trick_sequence()[0]

    @property
    def followers(self):
        return self.trick_sequence()[1:]

    def recorded_card(self, card):
        """Record a card as played and return it"""
        self.played_cards.append(card)
        return card

    def first_trick(self):
        trump = self.bid.trump
        lead_card = self.recorded_card(self.leader.lead(bid=self.bid))
        lead_suit = lead_card.effective_suit(trump)
        played_cards_values = []
        for player in self.followers:
            played_card = self.recorded_card(player.follow(
                current_winner=self.leader,
                leadsuit=lead_suit,
                trump=self.bid.trump,
                tricksequence=self.trick_sequence(),
                played_cards=self.played_cards,
            ))
            for p in self.players:
                p.sees_card(played_card)
                # All players update their known voids if the current
                # player is not following suit.
                # NOTE: This would be better if it could somehow be
                # assessed at the end of the trick. Otherwise,
                # players are playing as if people who have already
                # played in trick could trump in.
                if played_card.suit != lead_suit:
                    p.learns_void(player, lead_suit)
                # If player knows, based on played cards and own hand,
                # there's a void in a suit, this is registered as a void
                # for all players, only known to player.
                for suit in SUITS:
                    if len(limit_to_suit(p.cards_unseen, suit, trump)) == 0:
                        for p2 in self.players:
                            p.learns_void(p2, suit)
            if played_card.effective_suit(trump) == lead_suit:
                played_cards_values.append(played_card.value(trump))
            else:
                played_cards_values.append(-1)
            # the current winner number is the number of the player
            # in the tricksequence whose card value is currently
            # highest among all played cards.
            current_winner = self.trick_sequence()[
                played_cards_values.index(max(played_cards_values))
            ]

        return current_winner

    def normal_trick(self, winner):
        return winner

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
        topcard = self.deck.pop()
        for position, bidmaker in enumerate(self.bidders_in_order):
            method = getattr(bidmaker, bid_method)
            bid = method(
                player_position=position,
                topcard=topcard
            )
            if not bid.is_pass:
                return bid

        return None

    def _increment_trick_count(self, winner):
        for team in self.tricks:
            if winner in team:
                self.tricks[team] += 1

    def score_round(self):
        """Increment team scores and find a winner for the round."""
        for team in self.tricks:
            if team is not self.bidding_team:
                if self.tricks[team] > 2:
                    self.scores[team] += 2
            elif self.bid.is_alone:
                if self.tricks[team] > 2:
                    self.scores[team] += 1
                if self.tricks[team] > 4:
                    self.scores[team] += 3
            else:
                if self.tricks[team] > 2:
                    self.scores[team] += 1
                if self.tricks[team] > 4:
                    self.scores[team] += 1

    @property
    def bidding_team(self):
        return self._team_for_player(self.bid.player)

    def _team_for_player(self, player):
        for team in self.tricks:
            if player in team:
                return team
