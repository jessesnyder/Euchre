from random import randint
from session import Session
from game import LivePlayerSession
from liveplayer import LivePlayer
from deck import Deck
from deck import SUITS
from score import score_round
from score import undo_score_round
from ui import ConsoleUI


# This section is for setting global variables and importing methods.

# card_values = [(x, y) for x in range(4) for y in range(6)]
# suitlabels = ['Hearts', 'Spades', 'Diamonds', 'Clubs']
# Having same-color suits two apart enables actions recognizing their
# complementary relationship in Euchre.
# positionlabels = ['9', '10', 'Jack', 'Queen', 'King', 'Ace']
name = ""
hands = 0
hand = 0
bidding_data = []

POINTS_TO_WIN_GAME = 10
NO_BID = 999


# This section is for defining global functions.
def print_card(card):
    """ UI-appropriate view of a Card """
    return str('the ' + card.position + ' of ' + card.suit)


def run(lpactive=False, num_games=200):
    """ Runs the games. """
    ui = ConsoleUI()
    if lpactive:
        session = LivePlayerSession(ui, num_games)
    else:
        session = Session(ui, num_games)

    # Start game.
    session.start()

    positions = [0, 1, 2, 3]

    team1score = 0
    team2score = 0
    teamscores = [team1score, team2score]

    game = 0
    topcard = []

    for game in session.games:
        game.start_round()

    result = "Team1 game wins = {0}, Team2 game wins = {1}".format(
        Team1.gamescore,
        Team2.gamescore
    )
    if lpactive:
        print(result)

    return result
