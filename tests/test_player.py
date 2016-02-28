from unittest import TestCase
from player import Player
from team import Team
from deck import Card


class TestPlayerInit(TestCase):
    """ Does a Player basically work? """

    def test_initialization(self):
        john = Player("John", 1)
        self.assertFalse(john.isDealer)
        self.assertEqual(john.handvalue, 0)
        self.assertIsNone(john.partner)
        self.assertEqual(john.name, "John")


class TestBidding(TestCase):
    """ We're not testing hand scoring in minute detail here.
        We just want to verify the obvious cases work.
    """

    bad_cards = (
        Card('9', 'Hearts'),
        Card('9', 'Diamonds'),
        Card('9', 'Spades'),
        Card('9', 'Clubs'),
        Card('10', 'Hearts')
    )

    great_cards = (
        Card('Ace', 'Hearts'),
        Card('Ace', 'Diamonds'),
        Card('Jack', 'Hearts'),
        Card('Jack', 'Diamonds'),
        Card('King', 'Hearts')
    )

    def _player_on_team(self):
        john = Player("John", 1)
        Team(1, (john, Player("Jane", 3)))

        return john

    def test_bid_first_round_with_horrible_hand_passes(self):
        john = self._player_on_team()
        for card in self.bad_cards:
            john.add_card(card)

        bid = john.bid_first_round(
            player_position=0, topcard=Card('10', 'Spades')
        )

        self.assertTrue(bid.is_pass)

    def test_bid_first_round_with_amazing_hand_goes_alone(self):
        john = self._player_on_team()
        for card in self.great_cards:
            john.add_card(card)

        bid = john.bid_first_round(
            player_position=0, topcard=Card('Queen', 'Hearts')
        )

        self.assertTrue(bid.is_alone)

    def test_bid_second_round_with_horrible_hand_passes(self):
        john = self._player_on_team()
        for card in self.bad_cards:
            john.add_card(card)

        bid = john.bid_second_round(
            player_position=0, topcard=Card('10', 'Spades')
        )

        self.assertTrue(bid.is_pass)

    def test_bid_second_round_with_amazing_hand_goes_alone(self):
        john = self._player_on_team()
        for card in self.great_cards:
            john.add_card(card)

        bid = john.bid_second_round(
            player_position=0, topcard=Card('Queen', 'Spades')
        )

        self.assertTrue(bid.is_alone)
