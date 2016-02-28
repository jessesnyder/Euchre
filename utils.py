"""utils should have no intra-project dependencies"""


def group_players_as_teams(players):
    """Group 4 players into two teams"""
    return ((players[0], players[2]), (players[1], players[3]))


def next_in_rotation(sequence, current_index):
    """Return the next item in the rotation given the current active
       index. If the current index is the last, return the first.
    """
    next_index = current_index + 1
    if next_index >= len(sequence):
        return sequence[0]
    return sequence[next_index]
