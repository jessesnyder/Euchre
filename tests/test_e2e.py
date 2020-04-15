from euchre import Euchre15


def test_end_to_end():
    result = Euchre15.run(2, 1)
    scores = [result[0].gamescore, result[1].gamescore]
    assert scores[0] + scores[1] == 1
