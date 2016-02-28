"""utils should have no intra-project dependencies"""


def group_players_as_teams(players):
    """Group 4 players into two teams"""
    return ((players[0], players[2]), (players[1], players[3]))
