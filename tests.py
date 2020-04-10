def test_end_to_end():
    import Euchre15
    scores = [Euchre15.Teams[0].gamescore, Euchre15.Teams[1].gamescore]
    assert scores[0] + scores[1] == 1
