"""test_trickset.py"""
from unittest import TestCase
from bid import Bid
from deck import Deck
from player import Player
from trickset import Trickset


class StubBidder(Player):

    def __init__(self, name):
        super(StubBidder, self).__init__(name, 1)


class AlwaysBids(StubBidder):

    def bid_first_round(self, player_position, topcard):
        return Bid.a_bid(self, topcard.suit)

    def bid_second_round(self, player_position, topcard):
        return Bid.a_bid(self, topcard.suit)


class AlwaysPasses(StubBidder):

    def bid_first_round(self, player_position, topcard):
        return Bid.a_pass(self)

    def bid_second_round(self, player_position, topcard):
        return Bid.a_pass(self)


class TricksetTest(TestCase):

    def _make_one(self):
        players = (
            Player("Amy"), Player("Bonnie"), Player("Andy"), Player("Bill")
        )

        return Trickset(
            players=players,
            dealer=players[0],
            deck=Deck(),
        )

    def test_bidders_in_order(self):
        players = (
            Player("Amy"), Player("Bonnie"), Player("Andy"), Player("Bill")
        )
        t = Trickset(players=players, dealer=players[2], deck=Deck())

        self.assertEqual(
            (t.players[3], t.players[0], t.players[1], t.players[2]),
            t.bidders_in_order
        )

    def test_run_bidding_1_someone_bids_returns_bid(self):
        p1 = AlwaysBids("Bidder")
        p2, p3, p4 = [AlwaysPasses("Passer " + str(i)) for i in range(3)]
        g = Trickset(players=(p1, p2, p3, p4), dealer=p1, deck=Deck())

        bid = g.run_bidding_round_1()

        self.assertEqual(p1, bid.player)

    def test_run_bidding_1_no_one_bids_returns_none(self):
        p1, p2, p3, p4 = [AlwaysPasses("Passer " + str(i)) for i in range(4)]
        g = Trickset(players=(p1, p2, p3, p4), dealer=p1, deck=Deck())

        bid = g.run_bidding_round_1()

        self.assertIsNone(bid)

    def test_run_bidding_2_someone_bids_returns_bid(self):
        p1 = AlwaysBids("Bidder")
        p2, p3, p4 = [AlwaysPasses("Passer " + str(i)) for i in range(3)]
        g = Trickset(players=(p1, p2, p3, p4), dealer=p1, deck=Deck())

        bid = g.run_bidding_round_2()

        self.assertEqual(p1, bid.player)

    def test_run_bidding_2_no_one_bids_returns_none(self):
        p1, p2, p3, p4 = [AlwaysPasses("Passer " + str(i)) for i in range(4)]
        g = Trickset(players=(p1, p2, p3, p4), dealer=p1, deck=Deck())

        bid = g.run_bidding_round_2()

        self.assertIsNone(bid)
