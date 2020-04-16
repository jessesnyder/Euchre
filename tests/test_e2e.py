from euchre import Euchre15


def test_end_to_end():
    num_games = 2
    result = Euchre15.run(have_real_player=False, games=num_games)
    scores = [result[0].gamescore, result[1].gamescore]
    assert scores[0] + scores[1] == num_games
