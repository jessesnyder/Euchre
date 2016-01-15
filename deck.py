from collections import Sequence
from random import shuffle


CARD_VALUES = [(x, y) for x in range(4) for y in range(6)]
# Having same-color suits two apart enables actions recognizing their
# complementary relationship in Euchre.
SUITLABELS = ['Hearts', 'Spades', 'Diamonds', 'Clubs']
POSITIONLABELS = ['9', '10', 'Jack', 'Queen', 'King', 'Ace']
CARDS_PER_HAND = 5


class Card():

    def __init__(self, count, suit):
        self.count = count
        self.suit = suit

    def __repr__(self):
        return "<{0} of {1}>".format(self.count, self.suit)


class Deck(Sequence):

    def __init__(self):
        self._cards = []
        for value in POSITIONLABELS:
            for suit in SUITLABELS:
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
