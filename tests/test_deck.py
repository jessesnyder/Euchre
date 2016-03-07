from unittest import TestCase
from deck import Card
from deck import Deck


class TestDeck(TestCase):

    def test_after_shuffle_top_card_different(self):
        deck = Deck()
        top = deck.pop()
        deck.shuffle()
        self.assertNotEqual(top, deck.pop())

    def test_next_issues_new_cards(self):
        deck = Deck()
        top = deck.pop()
        self.assertNotEqual(top, deck.pop())

    def test_remove(self):
        deck = Deck()
        card = Card(suit="Hearts", position="Queen")
        deck.remove(card)
        self.assertFalse(card in deck)
