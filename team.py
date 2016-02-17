"""Class Team."""
from collections import Sequence


class Team(Sequence):

    def __init__(self, number, players):
        self.name = "Team " + str(number)
        self.number = number
        self.score = 0
        self.trickscore = 0
        self.trickcount = 0
        self.gamescore = 0
        self.bid = 0
        self._players = players
        self._set_partners()
        self._set_team_on_players()

    def __getitem__(self, index):
        if index == 0:
            return self.playerA
        if index == 1:
            return self.playerB

        raise IndexError("Only two players on a team in Euchre.")

    def __len__(self):
        return len(self._players)

    def __repr__(self):
        return '<{0} "{1}" with {2} and {3}>'.format(
            self.__class__.__name__,
            self.name,
            self.playerA.name,
            self.playerB.name
        )

    def setopposingteam(self, team):
        for player in self._players:
            player.setopposingteam(team)

    def _set_partners(self):
        for player in self._players:
            others = [p for p in self._players if p is not player]
            for other in others:
                other.setpartner(player)

    def _set_team_on_players(self):
        for player in self._players:
            player.setteam(self)
