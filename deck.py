from collections import Sequence
from random import shuffle


CARD_VALUES = [(x, y) for x in range(4) for y in range(6)]
# Having same-color suits two apart enables actions recognizing their
# complementary relationship in Euchre.
SUITS = ('Hearts', 'Spades', 'Diamonds', 'Clubs')
POSITIONS = ('9', '10', 'Jack', 'Queen', 'King', 'Ace')
CARDS_PER_HAND = 5


def suits_trump_first(trump):
    suits = list(SUITS)
    return suits[suits.index(trump):] + suits[:suits.index(trump)]


def calc_card_point_value(trump_local, card):
    value = card.raw_value
    if card.is_right_bauer(trump_local):
        value += 16
    elif card.suit == trump_local:
        value += 6
    # Check for Left Bauer
    elif card.is_left_bauer(trump_local):
        value += 13  # Sets value of left bauer.

    return value


class Card():

    def __init__(self, position, suit):
        self.position = position
        self.suit = suit
        self.raw_value = POSITIONS.index(position)

    def __repr__(self):
        return "<{0} {1} of {2}>".format(
            self.__class__.__name__, self.position, self.suit
        )

    def is_right_bauer(self, trump=None):
        if trump is None:
            return False
        if self.position != 'Jack':
            return False
        if self.suit == trump:
            return True
        return False

    def is_left_bauer(self, trump=None):
        if trump is None:
            return False
        if self.position != 'Jack':
            return False
        if abs(SUITS.index(self.suit) - 2) == SUITS.index(trump):
            return True
        return False

    def is_same_suit(self, suit, trump):
        return self.suit == suit or self.is_left_bauer(trump)


class Deck(Sequence):

    def __init__(self):
        self._cards = []
        for value in POSITIONS:
            for suit in SUITS:
                self._cards.append(Card(value, suit))

        shuffle(self._cards)

    def __getitem__(self, index):
        return self._cards[index]

    def __len__(self):
        return len(self._cards)

    def pop(self):
        return self._cards.pop()

    def deal(self, players):
        for i in range(CARDS_PER_HAND):
            for player in players:
                player.add_card(self.pop())
