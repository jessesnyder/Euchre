"""Class Game."""
import random
from bid import Bid
from deck import Deck
from deck import SUITS
from player import Player
from trickset import Trickset
from liveplayer import LivePlayer
from team import Team
from utils import group_players_as_teams
from utils import next_in_rotation


BOT_PLAYER_NAMES = ['Sam', 'Kim', 'Sue', 'Tim']


class Session(object):
    """State and actions for a set of games"""

    def __init__(self, num_games):
        self.num_games = num_games
        self.players = self._build_players()
        self.teams = self._build_teams()
        self.deck = Deck()

    def _build_players(self):
        p0 = self._player0()
        p1 = Player(BOT_PLAYER_NAMES[1], 1)
        p2 = Player(BOT_PLAYER_NAMES[2], 2)
        p3 = Player(BOT_PLAYER_NAMES[3], 3)

        return (p0, p1, p2, p3)

    def _build_teams(self):
        team1 = Team(1, players=(self.players[0], self.players[2]))
        team2 = Team(2, players=(self.players[1], self.players[3]))

        team1.setopposingteam(team2)
        team2.setopposingteam(team1)

        return (team1, team2)

    def _player0(self):
        return Player(BOT_PLAYER_NAMES[0], 0)

    @property
    def games(self):
        for i in range(self.num_games):
            yield Game(self.teams, self.players, self.deck, self)

    def start(self):
        pass

    def output(self, string):
        pass


class LivePlayerSession(Session):
    """Interactive session with a live player"""

    liveplayer = None

    def __init__(self, num_games):
        super(LivePlayerSession, self).__init__(num_games)
        self.liveplayer = self.players[0]

    def start(self):
        print("Your partner is {0}.".format(self.liveplayer.partner.name))

    def _player0(self):
        return LivePlayer("You", 0)


class Game(object):
    """State and actions for a game."""

    _points_to_win_game = 10
    _cards_per_hand = 5

    def __init__(self, players, deck):
        self.deck = deck
        self.players = players
        self.team1, self.team2 = group_players_as_teams(self.players)
        self.scores = {
            self.team1: 0,
            self.team2: 0
        }
        self.current_dealer = None
        self.current_winner = None
        self.set_new_dealer()

    def new_trickset(self):
        self.deck.shuffle()
        self.set_new_dealer()
        return Trickset(
            players=self.players,
            dealer=self.current_dealer,
            deck=self.deck)

    def start_round(self):
        self.set_new_dealer()
        for team in self.teams:
            team.reset_scores()
        for player in self.players:
            player.reset_voids()

    @property
    def bidders_in_order(self):
        """Start with the next in line from the dealer"""
        leader_index = self.players.index(self.current_dealer) + 1
        return self.players[leader_index:] + self.players[:leader_index]

    def run_bidding_round_1(self):
        """ Return an actual bid or None """
        return self._run_bidding_round('bid_first_round')

    def run_bidding_round_2(self):
        """ Run bidding in suits of player's choice, if everyone passed
            in round 1
        """
        return self._run_bidding_round('bid_second_round')

    def _run_bidding_round(self, bid_method):
        topcard = self.deck[0]
        for position, bidmaker in enumerate(self.bidders_in_order):
            method = getattr(bidmaker, bid_method)
            bid = method(
                player_position=position,
                topcard=topcard
            )
            if not bid.is_pass:
                return bid

        return None

    def play(self):
        dealer = self.current_dealer
        topcard = self.deck[0]

        print("\n\nThe dealer is " + dealer.name + ".")
        print("\n\nThe up-card is " + topcard + ".")
        trump = topcard.suit
        round_one_bid = self.run_bidding_round_1()
        if round_one_bid is None:
            for player in self.players:
                player.updatecards_out(topcard)

            round_two_bid = self.run_bidding_round_2()
            if round_two_bid is None:
                print("No one bids. Redeal!")
                return

        else:
            # Playing
            trickcount = 1
            for trick in range(5):
                if lpactive:
                    print("\nTrick " + str(trickcount) + ": ")
                played_cards = []  # Cards played in trick
                played_cards_values = []  # Values of cards played in trick
                if trickcount == 1:
                    leader_num = firstbidder_num
                else:
                    leader_num = current_winner.number
                tricksequence = Players[leader_num:] + Players[0:leader_num]
                if bid_type == 2:
                    tricksequence.remove(bidmaker.partner)
                for player in tricksequence:
                    played_card = player.play(
                        current_winner=current_winner,
                        leadsuit=leadsuit,
                        trump=trump,
                        tricksequence=tricksequence,
                        played_cards=played_cards,
                        played_card_values=played_cards_values
                    )
                    if player == tricksequence[0]:
                        leadsuit = played_card.effective_suit(trump)
                    if lpactive:
                        print("{0} plays {1}.".format(
                            player.name,
                            print_card(played_card)
                        ))
                    played_cards.append(played_card)
                    if not played_card.suit == leadsuit:
                        for p in Players:
                            p.learns_void(player, leadsuit)  # All players update their known voids if the see current player not following suit. NOTE: This would be better if it could somehow be assessed at the end of the trick. Otherwise, players are playing as if people who have already played in trick could trump in.
                    for player2 in Players:
                        if not player2 == player:
                            player2.updatecards_out(played_card)  # All players update the cards they know are out.
                        for suit in SUITS:
                            if len(player2.getsuit(suit, player2.cards_out, trump)) == 0:
                                for p in Players:
                                    p.learns_void(player2, suit)  # If player knows, based on played cards and own hand, there's a void in a suit, this is registered as a void for all players, only known to player.
                    if played_card.effective_suit(trump) == leadsuit:
                        played_cards_values.append(played_card.value(trump))
                    elif played_card.suit == trump:
                        played_cards_values.append(played_card.value(trump))
                    else:
                        played_cards_values.append(-1)
                    # the current winner number is the number of the player
                    # in the tricksequence whose card value is currently
                    # highest among all played cards.
                    current_winner = tricksequence[
                        played_cards_values.index(max(played_cards_values))
                    ]
                current_winner.team.trickscore += 1
                trickcount += 1
                if lpactive:
                    print("\n" + current_winner.name + " wins trick!")

            roundwinner = score_round(teams)
            # End of round
            if lpactive:
                print(roundwinner.name + " wins round!")
                print("Team 1 score: " + str(Team1.score) + "; Team 2 score: " + str(Team2.score))
                print("Team 1 trick count:" + str(Team1.trickscore) + "; Team 2 trick count: " + str(Team2.trickscore))
            teamscores = [Team1.score, Team2.score]
            # This is the part where I'll try to make it possible to replay a hand.
            replay = 0
            while lpactive and not replay:
                try:
                    replay = input("\nReplay hand? (1 = no, 2 = yes)")
                except:
                    lpdiscard = 999

            if replay == 2:
                undo_score_round(teams)

            if max(teamscores) >= POINTS_TO_WIN_GAME:
                if lpactive:
                    print("Team " + str(teamscores.index(max(teamscores)) + 1) + " wins game " + str(game) + "!")
                teams[teamscores.index(max(teamscores))].gamescore += 1
                Team1.score = 0
                Team2.score = 0
                game += 1
                if lpactive:
                    print("END OF GAME " + str(game))
                    print(
                        "Team1 game wins = ",
                        Team1.gamescore,
                        " Team2 game wins = ",
                        Team2.gamescore
                    )

    def deal(self):
        self.deck.shuffle()
        self.deck.deal(self.players, self._cards_per_hand)

    def set_new_dealer(self):
        if self.current_dealer is None:
            self.current_dealer = random.choice(self.players)
        else:
            current_index = self.players.index(self.current_dealer)
            self.current_dealer = next_in_rotation(self.players, current_index)
        self.current_dealer.isDealer = True
