from unittest import TestCase
from player import Player
from bid import Bid


class TestBid(TestCase):
    """ This is a small, simple class """

    def test_trump_optional(self):
        john = Player("John", 1)
        bid = Bid(player=john, bidtype=Bid.PASS)
        self.assertEqual(bid.type, Bid.PASS)

    def test_with_trump(self):
        john = Player("John", 1)
        bid = Bid(player=john, bidtype=Bid.PASS, trump='Hearts')
        self.assertEqual(bid.type, Bid.PASS)

    def test_pass_constructor(self):
        john = Player("John", 1)
        a_pass = Bid.a_pass(john)

        self.assertTrue(a_pass.is_pass)
        self.assertFalse(a_pass.is_alone)

    def test_bid_constructor(self):
        john = Player("John", 1)
        bid = Bid.a_bid(john, trump='Hearts')
        self.assertFalse(bid.is_pass)
        self.assertFalse(bid.is_alone)

    def test_go_alone_constructor(self):
        john = Player("John", 1)
        go_alone = Bid.go_alone(john, trump='Spades')
        self.assertFalse(go_alone.is_pass)
        self.assertTrue(go_alone.is_alone)
