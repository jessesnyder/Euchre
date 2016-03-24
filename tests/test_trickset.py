"""test_trickset.py"""
from unittest import TestCase
from bid import Bid
from deck import Deck
from deck import SUITS
from player import Player
from trickset import Trickset


class StubBidder(Player):
    pass


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

    def test_deal_each_player_gets_5_cards(self):
        players = (
            Player("Amy"), Player("Bonnie"), Player("Andy"), Player("Bill")
        )
        t = Trickset(players=players, dealer=players[2])
        t.deal()

        for p in players:
            self.assertEqual(5, len(p.hand))

    def test_deal_each_players_hand_is_unique(self):
        players = (
            Player("Amy"), Player("Bonnie"), Player("Andy"), Player("Bill")
        )
        t = Trickset(players=players, dealer=players[2])
        t.deal()
        hands = [p.hand for p in players]
        for hand in [p.hand for p in players]:
            otherhands = [h for h in hands if h is not hand]
            for card in hand:
                for otherhand in otherhands:
                    self.assertNotIn(
                        card, otherhand, "hands had some of the same cards!"
                    )

    def test_bidders_in_order(self):
        players = (
            Player("Amy"), Player("Bonnie"), Player("Andy"), Player("Bill")
        )
        t = Trickset(players=players, dealer=players[2])
        t.deal()

        self.assertEqual(
            (t.players[3], t.players[0], t.players[1], t.players[2]),
            t.bidders_in_order
        )

    def test_run_bidding_1_someone_bids_returns_bid(self):
        p1 = AlwaysBids("Bidder")
        p2, p3, p4 = [AlwaysPasses("Passer " + str(i)) for i in range(3)]
        t = Trickset(players=(p1, p2, p3, p4), dealer=p1)
        t.deal()

        bid = t.run_bidding_round_1()

        self.assertEqual(p1, bid.player)
        self.assertIn(bid.trump, SUITS)

    def test_run_bidding_1_no_one_bids_returns_none(self):
        p1, p2, p3, p4 = [AlwaysPasses("Passer " + str(i)) for i in range(4)]
        t = Trickset(players=(p1, p2, p3, p4), dealer=p1)
        t.deal()

        bid = t.run_bidding_round_1()

        self.assertIsNone(bid)

    def test_run_bidding_2_someone_bids_returns_bid(self):
        p1 = AlwaysBids("Bidder")
        p2, p3, p4 = [AlwaysPasses("Passer " + str(i)) for i in range(3)]
        t = Trickset(players=(p1, p2, p3, p4), dealer=p1)
        t.deal()

        bid = t.run_bidding_round_2()

        self.assertEqual(p1, bid.player)

    def test_run_bidding_2_no_one_bids_returns_none(self):
        p1, p2, p3, p4 = [AlwaysPasses("Passer " + str(i)) for i in range(4)]
        t = Trickset(players=(p1, p2, p3, p4), dealer=p1)
        t.deal()

        bid = t.run_bidding_round_2()

        self.assertIsNone(bid)

    def test_trick_sequence_normal_bid_is_all_players_from_dealers_left(self):
        players = (
            Player("Amy"), Player("Bonnie"), Player("Andy"), Player("Bill")
        )
        t = Trickset(players=players, dealer=players[2])
        t.deal()
        t.bid = Bid.a_bid(player=players[0], trump='Hearts')
        self.assertEqual(
            (players[3], players[0], players[1], players[2]),
            t.trick_sequence()
        )

    def test_trick_sequence_going_alone_omits_bidders_partner(self):
        players = (
            Player("Amy"), Player("Bonnie"), Player("Andy"), Player("Bill")
        )
        t = Trickset(players=players, dealer=players[2])
        t.deal()
        t.bid = Bid.go_alone(player=players[0], trump='Hearts')

        self.assertEqual(
            (players[3], players[0], players[1]),
            t.trick_sequence()
        )

    def test_trick_sequence_with_winner_starts_with_winner(self):
        players = (
            Player("Amy"), Player("Bonnie"), Player("Andy"), Player("Bill")
        )
        t = Trickset(players=players, dealer=players[2])
        t.deal()
        t.bid = Bid.a_bid(player=players[0], trump='Hearts')

        self.assertEqual(
            (players[1], players[2], players[3], players[0]),
            t.trick_sequence(winner=players[1])
        )

    def test_trick_sequence_going_alone_omits_bidders_partner_with_winner(self):
        players = (
            Player("Amy"), Player("Bonnie"), Player("Andy"), Player("Bill")
        )
        t = Trickset(players=players, dealer=players[2])
        t.deal()
        t.bid = Bid.go_alone(player=players[0], trump='Hearts')

        self.assertEqual(
            (players[1], players[3], players[0]),
            t.trick_sequence(winner=players[1])
        )

    def test_first_trick_normal_bid(self):
        players = (
            Player("Amy"), Player("Bonnie"), Player("Andy"), Player("Bill")
        )
        t = Trickset(players=players, dealer=players[2])
        t.deal()
        t.bid = Bid.a_bid(player=players[0], trump='Hearts')
        winner = t.first_trick()

        self.assertIn(winner, players)

    def test_first_trick_going_alone(self):
        players = (
            Player("Amy"), Player("Bonnie"), Player("Andy"), Player("Bill")
        )
        t = Trickset(players=players, dealer=players[2])
        t.deal()
        t.bid = Bid.go_alone(player=players[0], trump='Hearts')
        winner = t.first_trick()

        self.assertIn(winner, (players[0], players[1], players[3]))
