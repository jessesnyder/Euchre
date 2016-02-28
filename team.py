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
        self.bid = None
        self._players = players
        self._set_partners()
        self._set_team_on_players()

    def __getitem__(self, index):
        return self._players[index]

    def __len__(self):
        return len(self._players)

    def __repr__(self):
        return '<{0} "{1}" with {2}>'.format(
            self.__class__.__name__,
            self.name,
            ', '.join(p.name for p in self._players)
        )

    def reset_scores(self):
        self.trickcount = 0
        self.trickscore = 0

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
