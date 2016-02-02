from random import randint
from player import Player
from liveplayer import LivePlayer
from team import Team
from deck import Deck


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

# from random import shuffle

BOT_PLAYER_NAMES = ['Sam', 'Kim', 'Sue', 'Tim']
NO_BID = 999


# This section is for defining global functions.
def print_card(card):
    """ UI-appropriate view of a Card """
    return str('the ' + card.position + ' of ' + card.suit)


def run(lpactive=False, games=200):
    if lpactive:
        Player0 = LivePlayer("You", 0)
    else:
        Player0 = Player(BOT_PLAYER_NAMES[0], 0)
    Player1 = Player(BOT_PLAYER_NAMES[1], 1)
    Player2 = Player(BOT_PLAYER_NAMES[2], 2)
    Player3 = Player(BOT_PLAYER_NAMES[3], 3)
    Players = [Player0, Player1, Player2, Player3]

    Team1 = Team(1, Player0, Player2)
    Team2 = Team(2, Player1, Player3)

    Team1.setopposingteam(Team2)
    Team2.setopposingteam(Team1)
    Teams = [Team1, Team2]

    # Start game.

    if lpactive:
        print("Your partner is {0}.".format(Player0.partner.name))

    positions = [0, 1, 2, 3]
    nextdealer_num = randint(0, 3)

    team1score = 0
    team2score = 0
    teamscores = [team1score, team2score]

    game = 0
    leadsuit = -1
    # NOTE: With respect to the function showhand,
    # bidding_round just serves to distinguish between when trump is known (0)
    # and when it isn't (1).
    bidding_round = 0
    # 1 == "no" XXX: this should be converted to a boolean right after input
    replay = 1
    topcard = []

    while game < games:
        # Dealing
        # if not(replay == 2):
        #     dealer_num = nextdealer_num
        dealer_num = nextdealer_num
        dealer = Players[dealer_num]
        dealer.isDealer = True

        if lpactive:
            print("\n\nThe dealer is " + dealer.name + ".")
        Team1.trickcount = 0
        Team2.trickcount = 0
        alone = 0
        shuffledcards = Deck()
        # for player in Players:
        #     player.getcards()
        shuffledcards.deal(Players)
        # if replay == 2:
        #     topcard = topcardbu[:]
        # else:
        #     topcard = shuffledcards[0]
        #     topcardbu = topcard[:]
        topcard = shuffledcards[0]
        trump = topcard.suit
        if lpactive:
            print("The up-card is " + print_card(topcard))
        for player in Players:
            if lpactive and player == 0:
                player.showhand(trump, 0)
        dealers = positions[dealer_num:] + positions[:dealer_num]
        nextdealer_num = Players[dealers[1]].number
        firstbidder_num = Players[dealers[1]].number
        bidders = positions[firstbidder_num:] + positions[:firstbidder_num]
        # Bidding
        bid = 0
        for bidder_num in bidders:
            bidmaker = Players[bidder_num]
            # Second parameter is "player position" in bidding order,
            # currently stored when recording live player data.
            # May have other uses.
            bid = bidmaker.bid(
                is_first_bidding_round=False,
                player_position=bidders.index(bidder_num),
                topcard=topcard
            )
            bid_type = bid[1]
            if bid_type > 0:
                dealer.hand.append(topcard)
                if isinstance(dealer, LivePlayer):
                    # If the LivePlayer needs to discard, the following
                    # is skipped. LP must be prompted to discard below.
                    pass
                else:
                    handbackup = dealer.hand[:]
                    discardvalues = []
                    for discard in range(6):
                        dealer.hand = handbackup[:]
                        del(dealer.hand[discard])
                        discardvalues.append(dealer.calc_handvalue(trump, 0))
                    dealer.hand = handbackup
                    # Discards from dealers hand the card that
                    # resulted in highest hand value when discarded.
                    del(dealer.hand[discardvalues.index(max(discardvalues))])
            if bid_type == 0:
                if lpactive:
                    print(bidmaker.name + " passes.")
                continue
            else:
                if bid_type == 2:
                    alone = 1
                action = " orders "
                if bidder_num == dealer_num:
                    action = " picks "
                if lpactive:
                    print(
                        bidmaker.name + action + "up " +
                        print_card(topcard) + (". Going alone" * alone) + "."
                    )
                if isinstance(dealer, LivePlayer):
                    validdiscards = [1, 2, 3, 4, 5, 6]
                    lpdiscard = 999
                    Player0.showhand(trump, 0)
                    while lpdiscard not in validdiscards:
                        try:
                            lpdiscard = input("\nWhich card do you want to discard? (1 through 6)")
                        except:
                            lpdiscard = 999
                    del Player0.hand[lpdiscard - 1]
            break
        if bid_type == 0:  # round of bidding in other suits, if bid_type is still 0.
            for bidder_num in bidders:
                bidmaker = Players[bidder_num]
                bidmaker.updatecards_out(topcard)
            for bidder_num in bidders:
                bidmaker = Players[bidder_num]
                bid = bidmaker.bid(1, bidders.index(bidder_num), topcard)
                trump = bid[0]
                bid_type = bid[1]
                if bid_type > 0:
                    bidmaker = bidmaker
                if bid_type == 0:
                    if lpactive:
                        print(bidmaker.name + " passes.")
                    continue
                else:
                    if bid_type == 2:
                        alone = 1
                    if lpactive:
                        print(bidmaker.name + " bids " + suitlabels[trump] + (" alone" * alone) + ".")
                    break
        if bid_type == 0:
            if lpactive:
                print("No one bids. Redeal!")
            continue
        else:
            # trumplist = [0, 1, 2, 3]
            # trumplist = trumplist[trump:] + trumplist[:trump]
            # LB = (trumplist[2], 2)
            # Playing
            trickcount = 1
            Team1.trickscore = 0
            Team2.trickscore = 0
            for player in Players:
                player.reset_voids()
            for trick in range(5):
                if lpactive:
                    print("\nTrick " + str(trickcount) + ": ")
                played_cards = []  # Cards played in trick
                played_cards_values = []  # Values of cards played in trick
                if trickcount == 1:
                    leader_num = firstbidder_num
                else:
                    leader_num = currentwinner_num
                tricksequence = Players[leader_num:] + Players[0:leader_num]
                import pdb; pdb.set_trace()
                if bid_type == 2:
                    tricksequence.remove(bidmaker.partner)
                for player in tricksequence:
                    played_card = player.play(
                        leadsuit=leadsuit,
                        trump=trump,
                        tricksequence=tricksequence
                    )
                    if player == tricksequence[0]:
                        leadsuit = played_card.suit
                        if played_card.is_left_bauer(trump):
                            leadsuit = trump
                    if lpactive:
                        print(player.name + " plays " + print_card(played_card) + ".")
                    played_cards.append(played_card)
                    if not played_card.suit == leadsuit:
                        for player2 in Players:
                            player2.voids[player.number][leadsuit] = 1  # All players update their known voids if the see current player not following suit. NOTE: This would be better if it could somehow be assessed at the end of the trick. Otherwise, players are playing as if people who have already played in trick could trump in.
                    for player2 in Players:
                        if not player2 == player:
                            player2.updatecards_out(played_card)  # All players update the cards they know are out.
                        for suit in range(4):
                            if len(player2.getsuit(suit, player2.cards_out, trump)) == 0:
                                for player3 in Players:
                                    player3.voids[player2.number][suit] = 1  # If player knows, based on played cards and own hand, there's a void in a suit, this is registered as a void for all players, only known to player.
                    if played_card.suit == leadsuit or played_card.is_left_bauer(trump):
                        played_cards_values.append(played_card.value(trump))
                    elif played_card[0] == trump:
                        played_cards_values.append(played_card.value(trump))
                    else:
                        played_cards_values.append(-1)
                    currentwinner_num = tricksequence[played_cards_values.index(max(played_cards_values))].number #i.e., the current winner number is the number of the player in the tricksequence whose card value is currently highest among all played cards.
                Players[currentwinner_num].team.trickscore += 1
                trickcount += 1
                if lpactive:
                    print("\n" + Players[currentwinner_num].name + " wins trick!")

            for team in Teams:
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
            # End of round
            if lpactive:
                print(roundwinner.name + " wins round!")
            if lpactive:
                print("Team 1 score: " + str(Team1.score) + "; Team 2 score: " + str(Team2.score))
            if lpactive:
                print("Team 1 trick count:" + str(Team1.trickscore) + "; Team 2 trick count: " + str(Team2.trickscore))
            teamscores = [Team1.score, Team2.score]
            # This is the part where I'll try to make it possible to replay a hand.
            replay = 0
            while not replay:
                try:
                    replay = input("\nReplay hand? (1 = no, 2 = yes)")
                except:
                    lpdiscard = 999

            if replay == 2:
                for team in Teams:
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

            if max(teamscores) > 9:
                if lpactive:
                    print("Team " + str(teamscores.index(max(teamscores)) + 1) + " wins game " + str(game) + "!")
                Teams[teamscores.index(max(teamscores))].gamescore += 1
                Team1.score = 0
                Team2.score = 0
                game += 1
                if lpactive:
                    print("END OF GAME " + str(game))
                if lpactive:
                    print(
                        "Team1 game wins = ",
                        Team1.gamescore,
                        " Team2 game wins = ",
                        Team2.gamescore
                    )

    if lpactive:
        print("Team1 game wins = ", Team1.gamescore, " Team2 game wins = ", Team2.gamescore)


if __name__ == "__main__":
    run()
