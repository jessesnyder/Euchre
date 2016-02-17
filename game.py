"""Class Game."""
from random import randint
from deck import Deck
from player import Player
from liveplayer import LivePlayer
from team import Team

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
        self.players = (p0, p1, p2, p3)

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
            yield Game(self)


class LivePlayerSession(Session):
    """Interactive session with a live player"""

    def _player0(self):
        return LivePlayer("You", 0)


class Game(object):
    """State and actions for a game."""

    cards_per_hand = 5

    def __init__(self, session):
        self.current_dealer = self._choose_random_player()
        self.players = session.players
        self.deck = session.deck

    def _choose_random_player(self):
        return self.players[randint(len(self.players))]

    def deal(self):
        self.deck.shuffle()
        self.deck.deal(self.players, self.cards_per_hand)

    def rotate_dealer(self):
        self.current_dealer = self.players[self.current_dealer.number + 1]
