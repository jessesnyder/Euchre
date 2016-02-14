import sys
from Euchre15 import run


def interactive():
    """ Ask some questions to set up a game. """
    realplayer = False
    games = None
    realplayerInput = None

    while realplayerInput is None:
        realplayerInput = raw_input("Do you want to be a player? (y)es, (n)o: ")
        realplayerInput = realplayerInput.lower()
        if realplayerInput.startswith('q'):
            sys.exit()
        if realplayerInput.startswith('y'):
            realplayer = True

    while games is None:
        try:
            games = int(raw_input("How many games? "))
        except:
            print("A number, please.")
            continue
        if games > 200 and realplayer:
            games = None
            print("Too many!")
            continue
        if games < 0:
            games = None
            continue

    print run(realplayer, games)


if __name__ == "__main__":
    interactive()
