from unittest import TestCase
from deck import Card
from deck import Deck


class TestDeck(TestCase):

    def test_remove(self):
        deck = Deck()
        card = Card(suit="Hearts", position="Queen")
        deck.remove(card)
        self.assertFalse(card in deck)
