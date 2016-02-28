from unittest import TestCase
from player import Player
from bid import Bid
from team import Team
from game import Game
from deck import Deck
from deck import SUITS
from game import Session


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


class TestGame(TestCase):

    def _make_one(self):
        players = (
            Player("Amy"), Player("Bonnie"), Player("Andy"), Player("Bill")
        )

        return Game(
            players=players,
            deck=Deck(),
        )

    def test_scores_zero_before_first_round(self):
        game = self._make_one()
        self.assertEqual(0, game.scores[game.team1])
        self.assertEqual(0, game.scores[game.team2])

    def test_new_trickset_dealer_is_some_player(self):
        game = self._make_one()
        round1 = game.new_trickset()
        self.assertIn(round1.dealer, game.players)

    def test_dealer_rotates_by_round(self):
        game = self._make_one()
        round1 = game.new_trickset()
        round2 = game.new_trickset()
        self.assertNotEqual(round1.dealer, round2.dealer)


class TestGameBidding(TestGame):

    def test_bidders_in_order(self):
        g = self._make_one()
        g.current_dealer = g.players[2]

        self.assertEqual(
            (g.players[3], g.players[0], g.players[1], g.players[2]),
            g.bidders_in_order
        )

    def test_run_bidding_1_someone_bids_returns_bid(self):
        p1 = AlwaysBids("Bidder")
        p2, p3, p4 = [AlwaysPasses("Passer " + str(i)) for i in range(3)]
        g = Game(players=(p1, p2, p3, p4), deck=Deck())

        bid = g.run_bidding_round_1()

        self.assertEqual(p1, bid.player)

    def test_run_bidding_1_no_one_bids_returns_none(self):
        p1, p2, p3, p4 = [AlwaysPasses("Passer " + str(i)) for i in range(4)]
        g = Game(players=(p1, p2, p3, p4), deck=Deck())

        bid = g.run_bidding_round_1()

        self.assertIsNone(bid)

    def test_run_bidding_2_someone_bids_returns_bid(self):
        p1 = AlwaysBids("Bidder")
        p2, p3, p4 = [AlwaysPasses("Passer " + str(i)) for i in range(3)]
        g = Game(players=(p1, p2, p3, p4), deck=Deck())

        bid = g.run_bidding_round_2()

        self.assertEqual(p1, bid.player)

    def test_run_bidding_2_no_one_bids_returns_none(self):
        p1, p2, p3, p4 = [AlwaysPasses("Passer " + str(i)) for i in range(4)]
        g = Game(players=(p1, p2, p3, p4), deck=Deck())

        bid = g.run_bidding_round_2()

        self.assertIsNone(bid)
