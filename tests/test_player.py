from unittest import TestCase
from player import Player
from team import Team
from deck import Card


class TestPlayer(TestCase):
    """ Does a Player basically work? """

    def test_initialization(self):
        john = Player("John")
        self.assertFalse(john.isDealer)
        self.assertEqual(john.handvalue, 0)
        self.assertIsNone(john.partner)
        self.assertEqual(john.name, "John")

    def test_known_void_suit_count_zero_by_default(self):
        john = Player("John")
        mary = Player("Mary")

        self.assertEqual(0, john.known_void_suit_count(mary))

    def test_known_void_suit_totals_voids(self):
        john = Player("John")
        mary = Player("Mary")
        john.learns_void(mary, 'Hearts')
        john.learns_void(mary, 'Spades')

        self.assertEqual(2, john.known_void_suit_count(mary))

    def test_known_to_have_voids_returns_false_by_default(self):
        john = Player("John")
        mary = Player("Mary")

        self.assertFalse(john.known_to_have_voids(mary))

    def test_known_to_have_voids_returns_true_after_learning_void(self):
        john = Player("John")
        mary = Player("Mary")
        john.learns_void(mary, 'Hearts')

        self.assertTrue(john.known_to_have_voids(mary))

    def test_known_to_be_void_in_returns_false_by_default(self):
        john = Player("John")
        mary = Player("Mary")

        self.assertFalse(john.known_to_be_void_in(mary, 'Hearts'))

    def test_known_to_be_void_in_returns_true_after_learning_void(self):
        john = Player("John")
        mary = Player("Mary")
        john.learns_void(mary, 'Hearts')

        self.assertTrue(john.known_to_be_void_in(mary, 'Hearts'))

    def test_known_to_be_void_in_examines_suit(self):
        john = Player("John")
        mary = Player("Mary")
        john.learns_void(mary, 'Hearts')

        self.assertFalse(john.known_to_be_void_in(mary, 'Spades'))


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

    def _player_with_partner(self):
        p = Player("John")
        p.partner = Player("Joe")
        return p

    def test_bid_first_round_with_horrible_hand_passes(self):
        john = self._player_with_partner()
        for card in self.bad_cards:
            john.add_card(card)

        bid = john.bid_first_round(
            player_position=0, topcard=Card('10', 'Spades')
        )

        self.assertTrue(bid.is_pass)

    def test_bid_first_round_with_amazing_hand_goes_alone(self):
        john = self._player_with_partner()
        for card in self.great_cards:
            john.add_card(card)

        bid = john.bid_first_round(
            player_position=0, topcard=Card('Queen', 'Hearts')
        )

        self.assertTrue(bid.is_alone)

    def test_bid_second_round_with_horrible_hand_passes(self):
        john = self._player_with_partner()
        for card in self.bad_cards:
            john.add_card(card)

        bid = john.bid_second_round(
            player_position=0, topcard=Card('10', 'Spades')
        )

        self.assertTrue(bid.is_pass)

    def test_bid_second_round_with_amazing_hand_goes_alone(self):
        john = self._player_with_partner()
        for card in self.great_cards:
            john.add_card(card)

        bid = john.bid_second_round(
            player_position=0, topcard=Card('Queen', 'Spades')
        )

        self.assertTrue(bid.is_alone)
