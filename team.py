
class Team():
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
