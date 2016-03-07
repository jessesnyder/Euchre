"""Class Game."""
from collections import namedtuple
import random
from deck import Deck
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


GameResult = namedtuple("GameResult", "scores")


class Game(object):
    """State and actions for a game."""

    POINTS_TO_WIN = 10
    _cards_per_hand = 5

    def __init__(self, players):
        self.players = players
        self.team1, self.team2 = group_players_as_teams(self.players)
        self.scores = {
            self.team1: 0,
            self.team2: 0
        }
        self.current_dealer = None
        self.current_winner = None
        self.set_new_dealer()

    @property
    def over(self):
        return max(self.scores.values()) >= self.POINTS_TO_WIN

    def new_trickset(self):
        """Factory for Tricksets, which are played until the game score
           or one team is high enough to win the game.
        """
        self.set_new_dealer()
        return Trickset(players=self.players, dealer=self.current_dealer)

    def update_results(self, result):
        """Update the game score based on a Trickset (a round or deal)."""
        for team in (self.team1, self.team2):
            self.scores[team] += result.scores[team]

    def result(self):
        """Return the result of a completed game."""
        if not self.over:
            raise Exception("Game is not over!")

        return GameResult(scores=self.scores.copy())

    def set_new_dealer(self):
        if self.current_dealer is None:
            self.current_dealer = random.choice(self.players)
        else:
            current_index = self.players.index(self.current_dealer)
            self.current_dealer = next_in_rotation(self.players, current_index)
        self.current_dealer.isDealer = True
