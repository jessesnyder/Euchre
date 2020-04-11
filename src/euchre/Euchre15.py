# Lead Strategies Class
# Play Strateges Class

# Input Class
# Showcards Class
# class Showcards
# This section is for setting global variables and importing methods.

card_values = [(x, y) for x in range(4) for y in range(6)]
suitlabels = [
    "Hearts",
    "Spades",
    "Diamonds",
    "Clubs",
]  # Having same-color suits two apart enables actions recognizing their complementary relationship in Euchre.
positionlabels = ["9", "10", "Jack", "Queen", "King", "Ace"]
Playernames = ["Sam", "Kim", "Sue", "Tim"]
realplayer = 0
name = ""
hands = 0
hand = 0
bidding_data = []
games = 0
game = 0
leadsuit = -1
lpactive = 0  # By default, there's no live player.
bidding_round = 0  # NOTE: With respect to the function showhand, bidding_round just serves to distinguish between when trump is known (0) and when it isn't (1).
topcard = []

from random import shuffle
from random import randint


# This section is for defining global functions.


def labelcard(suit, position):
    "Labels cards in a way comprehensible to user."
    return str("the " + positionlabels[position] + " of " + suitlabels[suit])


def calc_card_point_value(trump_local, card_local):
    value = card_local[1]
    if card_local[0] == trump_local:
        if card_local[1] == 2:
            value += 16
        else:
            value += 6
    if abs(card_local[0] - trump_local) == 2 and card_local[1] == 2:
        value += 13  # Sets value of left bauer.
    return value


# This section is for defining object classes.


class Player:
    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.voids = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.handvalue = 0
        self.handbu = []

    def getcards(self):
        self.hand = []
        for card in range(5):
            self.hand.append(shuffledcards.pop())
            self.cards_out = card_values[:]
        for card in self.hand:
            del self.cards_out[self.cards_out.index(card)]
        self.handbu = self.hand[:]
        self.cards_outbu = self.cards_out[:]

    def getsuit(self, suit, cards, trump_local):
        self.cardlist = []
        trumplist = [0, 1, 2, 3]
        trumplist = trumplist[trump_local:] + trumplist[:trump_local]
        LB_local = (trumplist[2], 2)
        for card in cards:
            if card == LB_local:
                if suit == trump_local:
                    self.cardlist.append(card)
            else:
                if card[0] == suit:
                    self.cardlist.append(card)
        return self.cardlist

    def setpartner(self, partner):
        self.partner = partner

    def setteam(self, team):
        self.team = team

    def setopposingteam(self, team):
        self.opposingteam = team

    def updatecards_out(self, card):
        del self.cards_out[self.cards_out.index(card)]

    def getcardvalues(self, trump_local):
        self.cardvalues = []
        for card in self.hand:
            value = calc_card_point_value(trump_local, card)
            self.cardvalues.append(value)
        return self.cardvalues

    def calc_handvalue(self, trump_local, bidding_round):
        "Totals up hand value based on particular assumption of trump."
        self.handvalue = 0
        trial_hand = self.hand[:]
        if bidding_round == 0 and self.number == dealer_num:
            trial_hand.append(topcard)
        trumplist = [0, 1, 2, 3]
        trumplist = trumplist[trump_local:] + trumplist[:trump_local]
        LB_local = (trumplist[2], 2)
        suitcounts = [0, 0, 0, 0]
        for card in trial_hand:
            if card == LB_local:
                suitcounts[trump_local] += 1
            else:
                suitcounts[card[0]] += 1
        # Calculate temporary card values.
        discardvalues = [9] * len(trial_hand)
        count = 0
        for card in trial_hand:
            if not (card[0] == trump_local) and not card == LB_local:
                discardvalues[count] = (card[1] - 4.5) / pow(
                    suitcounts[card[0]], 3
                )  # formula computes value of all non-trump card values by subtracting 4.5 from positional value, then dividing by the cube of all cards in that suit.
            count += 1
        if len(trial_hand) == 6:
            del trial_hand[discardvalues.index(min(discardvalues))]
        for card in trial_hand:
            self.handvalue += calc_card_point_value(trump_local, card)
            if card[1] < 5 and card[1] > 0:
                self.handvalue -= (
                    1  # reduces value of 10 through King for bidding purposes
                )
        trumpvoid = 1
        if suitcounts[trump_local] > 0:
            trumpvoid = 0
        if not (trumpvoid):
            for suit in range(0, 4):
                if suitcounts[suit] == 0 and not (suit == trump_local):
                    self.handvalue += 6
        if bidding_round == 0:
            if (
                self.partner.number == dealer_num
            ):  # Extra points for adding up-card to hand or to partner's hand.
                self.handvalue += calc_card_point_value(trump_local, topcard) + 3
            if self.opposingteam == Players[dealer_num].opposingteam:
                self.handvalue -= (
                    calc_card_point_value(trump_local, topcard) + 3
                )  # Negative points for adding up-card to opposing team's hand, plus extra penalty (3) for possibility they'll create a void.
        return self.handvalue

    def showhand(self, trump_local, bidding_round):
        if isinstance(self, LivePlayer):
            print("\nYour hand:")
        else:
            print("\n" + self.name + "'s hand:")
        self.hand.sort(key=lambda card: card[1])  # sort by position
        self.hand.sort(key=lambda card: card[0])  # sort by suit
        LB_local = (999, 999)
        if (
            bidding_round == 0 and trump_local > -1
        ):  # NOTE: Bidding round is 0 in first round of bidding and after a bid is made
            trumpcards = []
            trumplist = [0, 1, 2, 3]
            trumplist = trumplist[trump_local:] + trumplist[:trump_local]
            LB_local = (trumplist[2], 2)  # left bauer
            for card in self.hand:
                if card[0] == trump_local or card == LB_local:
                    trumpcards.append(card)
            selfhandmatch = self.hand[:]
            for card in selfhandmatch:
                if card in trumpcards:
                    del self.hand[
                        self.hand.index(card)
                    ]  # removes trump cards from self.hand
            trumpcardvalues = []
            trumpcards2 = trumpcards[:]
            for card in trumpcards:
                trumpcardvalues.append(
                    calc_card_point_value(trump_local, card)
                )  # calculates values for trump cards

            def findkey(tup):
                return trumpcardvalues[
                    trumpcards2.index(tup)
                ]  # function returns value of trump card by matching position of the card tuple (suit, position) in an unchanging master list of trump cards

            trumpcards.sort(key=findkey)  # sorts trump cards according to their value
            for card in self.hand:
                trumpcards.append(
                    card
                )  # re-attaches cards from rest of hand to trump cards
            self.hand = trumpcards[:]  # assigns new values to self.hand from foregoing
        if self.hand[0] == LB_local:
            currentsuit = trump
        else:
            currentsuit = self.hand[0][0]
        print(suitlabels[currentsuit] + ":"),
        for card in self.hand:
            if card == LB_local:
                if not card == self.hand[0]:
                    print(","),  # ,end=''
                print("Jack of " + suitlabels[card[0]] + " [left bauer]"),  # ,end=""
            elif card[0] == currentsuit:
                if not card == self.hand[0]:
                    print(","),  # ,end=''
                print(
                    positionlabels[card[1]]
                    + (
                        (" of " + suitlabels[card[0]] + " [left bauer]")
                        * (card == LB_local)
                    )
                ),  # ,end=''
            else:
                currentsuit = card[0]
                print(
                    "\n" + suitlabels[card[0]] + ": " + positionlabels[card[1]]
                ),  # ,end=''
        print("\n")

    def bid(self, bidding_round, player_position):
        self.handval = 0
        if self.team == Team1:
            lowcutR0 = 36
            lowcutR1 = 33
            highcutR0 = 49
            highcutR1 = 46
        else:
            lowcutR0 = 36
            lowcutR1 = 33
            highcutR0 = 49
            highcutR1 = 46
        if bidding_round == 0:
            trump = topcard[0]
            self.handval = self.calc_handvalue(trump, 0)
            if self.handval > lowcutR0:
                if self.handval > highcutR0:
                    bid_type = 2
                else:
                    bid_type = 1
            else:
                bid_type = 0
        else:
            x = [0, 1, 2, 3]
            del x[topcard[0]]
            y = [0, 0, 0]
            count = 0
            for trump in x:
                y[count] = self.calc_handvalue(trump, 1)
                count += 1
            if max(y) > lowcutR1:
                if max(y) > highcutR1:
                    bid_type = 2
                else:
                    bid_type = 1
                trump = x[y.index(max(y))]
            #                print(self.name+" has hand value "+str(max(y)))
            else:
                bid_type = 0
        self.team.bid = bid_type
        return trump, bid_type

    def lead(self, trump_local):
        # picks a card for leading a trick
        lead_card_values = [0] * len(self.hand)
        count = 0
        trumplist = [0, 1, 2, 3]
        trumplist = trumplist[trump_local:] + trumplist[:trump_local]
        LB_local = (trumplist[2], 2)
        for card in self.hand:
            # This section to determine value of leading with trump cards.
            if card[0] == trump_local or card == LB_local:
                if self.partner == bidmaker or self == bidmaker:
                    lead_card_values[count] += 6
                else:
                    lead_card_values[count] -= 4
                higher = 0
                trumps_out = self.getsuit(trump_local, self.cards_out, trump_local)
                for card2 in trumps_out:
                    if calc_card_point_value(trump_local, card) < calc_card_point_value(
                        trump_local, card2
                    ):
                        higher += 1
                if higher == 0:
                    lead_card_values[
                        count
                    ] += 2  # card is higher than trump cards still out in other players hand (or discard pile)
                lead_card_values[count] -= higher
                lead_card_values[count] += (
                    len(self.getsuit(trump_local, self.hand, trump_local)) - 1
                )  # trump card value as lead increased by other trump in hand
                lead_card_values[count] -= 2 * (
                    sum(self.voids[self.number])
                )  # trump card value as lead descreased by voids in hand (missed opportunity to trump opponents' high off-suit cards)
                count += 1
            # This section to determine value of leading with non-trump cards.
            else:
                lower = 0
                higher = 0
                for card2 in self.getsuit(card[0], self.cards_out, trump_local):
                    if calc_card_point_value(trump_local, card) < calc_card_point_value(
                        trump_local, card2
                    ):
                        higher += 1
                    else:
                        lower += 1
                if higher == 0:
                    lead_card_values[count] += 2  # Card is high in suit.
                if (lower - higher) > 1:
                    lead_card_values[
                        count
                    ] += 1  # Of cards in same suit that are still out there, lower cards outnumber higher by more than 1.
                if higher > lower:
                    lead_card_values[
                        count
                    ] -= 1  # Of cards in same suit that are still out there, more are higher than lower.
                if (
                    sum(self.voids[self.partner.number]) > 0
                    and self.voids[self.partner.number][trump_local] == 0
                ):
                    lead_card_values[count] += 2  # My partner could trump in.
                if self.voids[self.opposingteam.playerA.number][card[0]] == 1:
                    if self.voids[self.opposingteam.playerA.number][trump_local] == 1:
                        lead_card_values[
                            count
                        ] += 1  # player in opposing team cannot beat, cannot trump
                    else:
                        lead_card_values[
                            count
                        ] -= 1  # player in opposing team has void, could possibly trump
                if self.voids[self.opposingteam.playerB.number][card[0]] == 1:
                    if self.voids[self.opposingteam.playerB.number][trump_local] == 1:
                        lead_card_values[
                            count
                        ] += 1  # player in opposing team cannot beat, cannot trump
                    else:
                        lead_card_values[
                            count
                        ] -= 1  # player in opposing team has void, could possibly trump
                if (
                    len(self.getsuit(card[0], self.hand, trump_local)) == 1
                    and len(self.getsuit(trump_local, self.hand, trump_local)) > 0
                ):
                    lead_card_values[
                        count
                    ] += 1  # could create a void in own hand, then trump
                count += 1
        leadcard = self.hand[lead_card_values.index(max(lead_card_values))]
        return leadcard  # NOTE-If highest value is found in more than one card, the first card in hand will be chosen.

    def follow(self, leadsuit_local, trump_local):
        follow_card_values = []
        validcards = self.getsuit(leadsuit_local, self.hand, trump_local)
        trumpcards = self.getsuit(trump_local, self.hand, trump_local)
        validcardvalues = []
        trumpcardvalues = []
        for validcard in validcards:
            validcardvalues.append(calc_card_point_value(trump_local, validcard))
        for trumpcard in trumpcards:
            trumpcardvalues.append(calc_card_point_value(trump_local, trumpcard))
        if validcards:
            lowcard = validcards[validcardvalues.index(min(validcardvalues))]
            highcard = validcards[validcardvalues.index(max(validcardvalues))]
        if trumpcards:
            lowtrump = trumpcards[trumpcardvalues.index(min(trumpcardvalues))]
            hightrump = trumpcards[trumpcardvalues.index(max(trumpcardvalues))]
        if validcards:
            if (
                Players[currentwinner_num] == self.partner
            ):  # If your partner is winning....
                partnercard = played_cards[tricksequence.index(self.partner)]
                for card in self.getsuit(leadsuit_local, self.cards_out, trump_local):
                    if calc_card_point_value(trump_local, card) > calc_card_point_value(
                        trump_local, partnercard
                    ):  # And there's a within-suit card still out that's higher than partner's.
                        # NOTE: This will sometimes lead to playing a higher card than necessary--if in last position, will play highest card even when a lower might be sure to win; and if partner is just one step below.
                        if calc_card_point_value(
                            trump_local, highcard
                        ) > calc_card_point_value(trump_local, partnercard):
                            return highcard  # ... and could lose to other in-suit card, then play my high card, if it beats partner's.
                else:
                    return lowcard
            else:  # If partner not winning....
                # NOTE: This will sometimes lead to playing a higher card than necessary.
                if calc_card_point_value(trump_local, highcard) > max(
                    played_cards_values
                ):
                    return highcard
                else:
                    return lowcard
        elif trumpcards:
            if (
                Players[currentwinner_num] == self.partner
            ):  # If your partner is winning....
                partnercard = played_cards[tricksequence.index(self.partner)]
                for card in self.getsuit(leadsuit_local, self.cards_out, trump_local):
                    if calc_card_point_value(trump_local, card) > calc_card_point_value(
                        trump_local, partnercard
                    ):
                        if calc_card_point_value(
                            trump_local, lowtrump
                        ) > calc_card_point_value(trump_local, partnercard):
                            return lowtrump  # ... and could lose to other in-suit card, then play my lowest trump card, if it beats partner's.
                        elif calc_card_point_value(
                            trump_local, hightrump
                        ) > calc_card_point_value(trump_local, partnercard):
                            return hightrump
            else:
                if calc_card_point_value(trump_local, lowtrump) > max(
                    played_cards_values
                ):
                    return lowtrump
                else:
                    if calc_card_point_value(trump_local, hightrump) > max(
                        played_cards_values
                    ):
                        return hightrump

        # If this point reached, cannot win trick. Play lowest card.
        for card in self.hand:
            follow_card_values.append(calc_card_point_value(trump_local, card))
            if self.getsuit(card[0], self.hand, trump_local) == 1:
                follow_card_values[len(follow_card_values)] -= 4
        followcard = self.hand[follow_card_values.index(min(follow_card_values))]
        return followcard

    def play(self, leadsuit_local, trump_local):
        if tricksequence.index(self) == 0:
            play_card = self.lead(trump_local)
        else:
            play_card = self.follow(leadsuit_local, trump_local)
        del self.hand[self.hand.index(play_card)]
        return play_card


class LivePlayer(Player):
    def __init__(self, name, number):
        self.name = name
        self.number = number
        self.voids = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]

    def bid(
        self, bidding_round, player_position
    ):  # Does this override bid for Player class?
        if bidding_round == 0:
            trump = topcard[0]
            handval = self.calc_handvalue(trump, 0)
            validbids = [0, 1, 2, 88]
            bid_type = 999
            while bid_type not in validbids:
                try:
                    bid_type = int(
                        input("\nDo you want to bid? (0=no; 1=yes; 2=go alone)")
                    )
                except ValueError:
                    bid_type = 999
            if bid_type == 88:
                Teams[0].score += 10
                bid_type = 1
            roundinfo = [
                bid_type,
                hand,
                bidding_round,
                player_position,
                handval,
                trump,
                topcard,
                self.hand,
            ]
            bidding_data.append(roundinfo)
            self.team.bid = bid_type
            return trump, bid_type
        else:
            self.showhand(-1, 1)
            validbids = [0, 1, 2]
            bid_type = 999
            while bid_type not in validbids:
                try:
                    bid_type = int(
                        input("\nDo you want to bid? (0=no; 1=yes; 2=go alone)")
                    )
                except ValueError:
                    bid_type = 999
            if bid_type > 0:
                validtrump = [0, 1, 2, 3]
                trump = 999
                del validtrump[topcard[0]]
                while trump not in validtrump:
                    try:
                        trump = int(
                            input(
                                "Which suit? (hearts=0, spades=1, diamonds=2, clubs=3)"
                            )
                        )
                    except ValueError:
                        trump = 999
                    if trump == topcard[0]:
                        print("You cannot bid " + suitlabels[topcard[0]] + ".")
                handval = self.calc_handvalue(trump, 1)
            else:
                x = [0, 1, 2, 3]
                del x[topcard[0]]
                y = [0, 0, 0]
                count = 0
                for trump in x:
                    y[count] = self.calc_handvalue(trump, 1)
                    count += 1
                handval = max(y)
                trump = x[y.index(max(y))]
                bid_type = 0
            roundinfo = [
                bid_type,
                hand,
                bidding_round,
                player_position,
                handval,
                trump,
                topcard,
                self.hand,
            ]
            bidding_data.append(roundinfo)
            self.team.bid = bid_type
            return trump, bid_type

    def play(self, leadsuit_local, trump_local):
        self.showhand(trump_local, 0)
        legit = [x + 1 for x in range(len(self.hand))]
        pc = 999
        trumplist = [0, 1, 2, 3]
        trumplist = trumplist[trump_local:] + trumplist[:trump_local]
        LB_local = (trumplist[2], 2)
        while pc not in legit:
            try:
                pc = int(input("Which card? (1 through " + str(len(self.hand)) + "): "))
            except ValueError:
                pc = 999
            if pc in legit:
                if tricksequence.index(self) > 0:
                    if len(self.getsuit(leadsuit_local, self.hand, trump_local)) > 0:
                        if self.hand[pc - 1] == LB_local and leadsuit == trump_local:
                            pass
                        elif self.hand[pc - 1][0] != leadsuit_local and (pc in legit):
                            print("Must follow lead suit.")
                            pc = 99
        play_card = self.hand[pc - 1]
        del self.hand[pc - 1]
        return play_card


class Team:
    def __init__(self, number):
        self.name = "Team " + str(number)
        self.number = number
        self.score = 0
        self.trickscore = 0
        self.gamescore = 0
        self.bid = 0
        # Bind players as attributes in team to players that exist outside the team. Otherwise, having players bid and play in order seemed too complicated.
        self.playerA = Players[number - 1]
        self.playerB = Players[number + 1]
        self.playerA.setpartner(self.playerB)
        self.playerB.setpartner(self.playerA)
        self.playerA.setteam(self)
        self.playerB.setteam(self)

    def setopposingteam(self, team):
        self.playerA.setopposingteam(team)
        self.playerB.setopposingteam(team)


# Get input from player.

# while not realplayer:
#     try:
#         realplayer = input("Do you want to be a player? 1=yes, 2= no): ")
#     except Exception:
#         realplayer == 0
#     if realplayer == "1":
#         Player0 = LivePlayer("You", 0)
#         lpactive = 1
#     elif realplayer == "2":
#         Player0 = Player(Playernames[0], 0)
#     else:
#         realplayer = 0

Player0 = Player(Playernames[0], 0)
Player1 = Player(Playernames[1], 1)
Player2 = Player(Playernames[2], 2)
Player3 = Player(Playernames[3], 3)
Players = [Player0, Player1, Player2, Player3]

Team1 = Team(1)
Team2 = Team(2)

Team1.setopposingteam(Team2)
Team2.setopposingteam(Team1)

Teams = [Team1, Team2]

# while not games:
#     try:
#         games = int(input("How many games?"))
#     except ValueError:
#         games = 0
#     if games > 200 and lpactive:
#         games = 0
#         print("Too many!")
#     if games < 0:
#         games = 0
games = 1

# Start game.

if lpactive:
    print("Your partner is Sue.")

positions = [0, 1, 2, 3]
nextdealer_num = randint(0, 3)

team1score = 0
team2score = 0
teamscores = [team1score, team2score]

while game < games:
    # Dealing
    dealer_num = nextdealer_num
    if lpactive:
        print("\n\nThe dealer is " + Players[dealer_num].name + ".")
    Team1.trickcount = 0
    Team2.trickcount = 0
    alone = 0
    shuffledcards = card_values[:]
    shuffle(shuffledcards)
    for player in Players:
        player.getcards()
    topcard = shuffledcards[0]
    topcardbu = topcard[:]
    trump = topcard[0]
    if lpactive:
        print("The up-card is " + labelcard(topcard[0], topcard[1]))
    for player in Players:
        if lpactive and player == 0:
            player.showhand(trump, 0)
    dealers = positions[dealer_num:] + positions[:dealer_num]
    nextdealer_num = Players[dealers[1]].number
    firstbidder_num = Players[dealers[1]].number
    bidders = positions[firstbidder_num:] + positions[:firstbidder_num]
    # Bidding
    bidding_round = 0
    bid = 0
    for bidder_num in bidders:
        bid = Players[bidder_num].bid(
            0, bidders.index(bidder_num)
        )  # Second parameter is "player position" in bidding order, currently stored when recording live player data. May have other uses.
        bid_type = bid[1]
        if bid_type > 0:
            bidmaker = Players[bidder_num]
            Players[dealer_num].hand.append(topcard)
            if isinstance(
                Players[dealer_num], LivePlayer
            ):  # If the LivePlayer needs to discard, the following is skipped. LP must be prompted to discard below.
                pass
            else:
                handbackup = Players[dealer_num].hand[:]
                discardvalues = []
                for discard in range(6):
                    Players[dealer_num].hand = handbackup[:]
                    del Players[dealer_num].hand[discard]
                    discardvalues.append(Players[dealer_num].calc_handvalue(trump, 0))
                Players[dealer_num].hand = handbackup
                del Players[dealer_num].hand[
                    discardvalues.index(max(discardvalues))
                ]  # Discards from dealers hand the card that resulted in highest hand value when discarded.
        if bid_type == 0:
            if lpactive:
                print(Players[bidder_num].name + " passes.")
            continue
        else:
            if bid_type == 2:
                alone = 1
            action = " orders "
            if bidder_num == dealer_num:
                action = " picks "
            if lpactive:
                print(
                    Players[bidder_num].name
                    + action
                    + "up "
                    + labelcard(topcard[0], topcard[1])
                    + (". Going alone" * alone)
                    + "."
                )
            if isinstance(Players[dealer_num], LivePlayer):
                validdiscards = [1, 2, 3, 4, 5, 6]
                lpdiscard = 999
                Player0.showhand(trump, 0)
                while lpdiscard not in validdiscards:
                    try:
                        lpdiscard = int(
                            input("\nWhich card do you want to discard? (1 through 6)")
                        )
                    except ValueError:
                        lpdiscard = 999
                del Player0.hand[lpdiscard - 1]
        break
    if bid_type == 0:  # round of bidding in other suits, if bid_type is still 0.
        for bidder_num in bidders:
            Players[bidder_num].updatecards_out(topcard)
        for bidder_num in bidders:
            bid = Players[bidder_num].bid(1, bidders.index(bidder_num))
            trump = bid[0]
            bid_type = bid[1]
            if bid_type > 0:
                bidmaker = Players[bidder_num]
            if bid_type == 0:
                if lpactive:
                    print(Players[bidder_num].name + " passes.")
                continue
            else:
                if bid_type == 2:
                    alone = 1
                if lpactive:
                    print(
                        Players[bidder_num].name
                        + " bids "
                        + suitlabels[trump]
                        + (" alone" * alone)
                        + "."
                    )
                break
    if bid_type == 0:
        if lpactive:
            print("No one bids. Redeal!")
        continue
    else:
        trumplist = [0, 1, 2, 3]
        trumplist = trumplist[trump:] + trumplist[:trump]
        LB = (trumplist[2], 2)
        # Playing
        trickcount = 1
        Team1.trickscore = 0
        Team2.trickscore = 0
        for player in Players:
            player.voids = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
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
            if bid_type == 2:
                tricksequence.remove(bidmaker.partner)
            for player in tricksequence:
                played_card = player.play(leadsuit, trump)
                if player == tricksequence[0]:
                    leadsuit = played_card[0]
                    if played_card == LB:
                        leadsuit = trump
                if lpactive:
                    print(
                        player.name
                        + " plays "
                        + labelcard(played_card[0], played_card[1])
                        + "."
                    )
                played_cards.append(played_card)
                if not (played_card[0]) == leadsuit:
                    for player2 in Players:
                        player2.voids[player.number][
                            leadsuit
                        ] = 1  # All players update their known voids if the see current player not following suit. NOTE: This would be better if it could somehow be assessed at the end of the trick. Otherwise, players are playing as if people who have already played in trick could trump in.
                for player2 in Players:
                    if not (player2 == player):
                        player2.updatecards_out(
                            played_card
                        )  # All players update the cards they know are out.
                    for suit in range(4):
                        if len(player2.getsuit(suit, player2.cards_out, trump)) == 0:
                            for player3 in Players:
                                player3.voids[player2.number][
                                    suit
                                ] = 1  # If player knows, based on played cards and own hand, there's a void in a suit, this is registered as a void for all players, only known to player.
                if played_card[0] == leadsuit or played_card == LB:
                    played_cards_values.append(
                        calc_card_point_value(trump, played_card)
                    )
                elif played_card[0] == trump:
                    played_cards_values.append(
                        calc_card_point_value(trump, played_card)
                    )
                else:
                    played_cards_values.append(-1)
                currentwinner_num = tricksequence[
                    played_cards_values.index(max(played_cards_values))
                ].number  # i.e., the current winner number is the number of the player in the tricksequence whose card value is currently highest among all played cards.
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
            print(
                "Team 1 score: "
                + str(Team1.score)
                + "; Team 2 score: "
                + str(Team2.score)
            )
        if lpactive:
            print(
                "Team 1 trick count:"
                + str(Team1.trickscore)
                + "; Team 2 trick count: "
                + str(Team2.trickscore)
            )
        teamscores = [Team1.score, Team2.score]

        if max(teamscores) > 9:
            if lpactive:
                print(
                    "Team "
                    + str(teamscores.index(max(teamscores)) + 1)
                    + " wins game "
                    + str(game)
                    + "!"
                )
            Teams[teamscores.index(max(teamscores))].gamescore += 1
            Team1.score = 0
            Team2.score = 0
            game += 1
            if lpactive:
                print("END OF GAME " + str(game))
            if lpactive:
                print(
                    "Team1 game wins=",
                    Team1.gamescore,
                    " Team2 game wins=",
                    Team2.gamescore,
                )

if lpactive:
    print("Team1 game wins=", Team1.gamescore, " Team2 game wins=", Team2.gamescore)
