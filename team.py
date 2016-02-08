"""Class Team."""

from collections import Sequence


class Team(Sequence):

    def __init__(self, number, playerA, playerB):
        self.name = "Team " + str(number)
        self.number = number
        self.score = 0
        self.trickscore = 0
        self.gamescore = 0
        self.bid = 0
        self.playerA = playerA
        self.playerB = playerB
        self.playerA.setpartner(self.playerB)
        self.playerB.setpartner(self.playerA)
        self.playerA.setteam(self)
        self.playerB.setteam(self)

    def __getitem__(self, index):
        if index == 0:
            return self.playerA
        if index == 1:
            return self.playerB

        raise IndexError("Only two players on a team in Euchre.")

    def __len__(self):
        return 2

    def setopposingteam(self, team):
        self.playerA.setopposingteam(team)
        self.playerB.setopposingteam(team)

    def __repr__(self):
        return '<{0} "{1}" with {2} and {3}>'.format(
            self.__class__.__name__,
            self.name,
            self.playerA.name,
            self.playerB.name
        )
