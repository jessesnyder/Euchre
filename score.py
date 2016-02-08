"""Class Score keeps track of scores."""


# class Score(object):
#     """Total up scores, find winners, etc."""

def score_round(teams):
    """Increment team scores and find a winner for the round."""
    for team in teams:
        if team.bid == 0:
            if team.trickscore > 2:
                team.score += 2
                roundwinner = team
        if team.bid == 1:
            if team.trickscore > 2:
                team.score += 1
                roundwinner = team
            if team.trickscore > 4:
                team.score += 1
        if team.bid == 2:
            if team.trickscore > 2:
                team.score += 1
                roundwinner = team
            if team.trickscore > 4:
                team.score += 3

    return roundwinner


def undo_score_round(teams):
    """Undo support for scoring."""
    for team in teams:
        if team.bid == 0:
            if team.trickscore > 2:
                team.score += (-2)
        if team.bid == 1:
            if team.trickscore > 2:
                team.score += (-1)
            if team.trickscore > 4:
                team.score += (-1)
        if team.bid == 2:
            if team.trickscore > 2:
                team.score += (-1)
            if team.trickscore > 4:
                team.score += (-3)
