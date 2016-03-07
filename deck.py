from collections import Sequence
from random import shuffle as r_shuffle


CARD_VALUES = [(x, y) for x in range(4) for y in range(6)]
# Having same-color suits two apart enables actions recognizing their
# complementary relationship in Euchre.
SUITS = ('Hearts', 'Spades', 'Diamonds', 'Clubs')
POSITIONS = ('9', '10', 'Jack', 'Queen', 'King', 'Ace')
CARDS_PER_HAND = 5


def suits_trump_first(trump=None):
    suits = list(SUITS)
    if trump is None:
        return suits

    return suits[suits.index(trump):] + suits[:suits.index(trump)]


def limit_to_suit(cards, suit, trump):
    """ Return just the cards in the specified suit, including
        the left bauer if the suit is the trump suit.
    """
    return tuple([card for card in cards if card.effective_suit(trump) == suit])


class Card(object):

    def __init__(self, position, suit):
        self.position = position
        self.suit = suit
        self.raw_value = POSITIONS.index(position)

    def __repr__(self):
        return "<{0} {1} of {2}>".format(
            self.__class__.__name__, self.position, self.suit
        )

    def __eq__(self, other):
        return self.suit == other.suit and self.position == other.position

    def effective_suit(self, trump):
        """ Return a trump aware suit for this Card. Basically, the left bauer
            returns the trump suit. All other cards return their "raw" suit.
        """
        if self.is_left_bauer(trump):
            return trump

        return self.suit

    def value(self, trump):
        """ Return a relative value for this Card. Not quite sure
            how this works.
        """
        if self.is_right_bauer(trump):
            return self.raw_value + 16

        if self.is_left_bauer(trump):
            return self.raw_value + 13

        if self.suit == trump:
            return self.raw_value + 6

        return self.raw_value

    def is_right_bauer(self, trump=None):
        return self.position == 'Jack' and self.suit == trump

    def is_left_bauer(self, trump=None):
        if trump is None or self.position != 'Jack':
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

        self.shuffle()

    def __getitem__(self, index):
        return self._cards[index]

    def __len__(self):
        return len(self._cards)

    def pop(self):
        """ Remove the top card """
        return self._cards.pop()

    def remove(self, card):
        """ Remove a specific card """
        if card in self._cards:
            self._cards.remove(card)

    def shuffle(self):
        """Yes, shuffle."""
        r_shuffle(self._cards)

    def deal(self, players, cards_per_hand):
        for i in range(cards_per_hand):
            for player in players:
                player.add_card(self.pop())
