

class Player():
    def __init__(self, name, number, isDealer=False):
        self.name = name
        self.number = number
        self.voids = [[0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0], [0, 0, 0, 0]]
        self.hand = []
        self.handvalue = 0
        self.handbu = []
        self.isDealer = isDealer

    def __repr__(self):
        partner = "(no partner)"
        if self.partner is not None:
            partner = self.partner.name

        return "<{0} {1}, partner of {2}>".format(
            self.__class__.__name__, self.name, partner
        )

    def add_card(self, card):
        self.hand.append(card)

    # def getcards(self):
    #     self.hand = []
    #     # if replay == 2:
    #     #     self.hand = self.handbu[:]
    #     #     self.cards_out = self.cards_outbu[:]
    #     # else:
    #     #     for card in range(5):
    #     #         self.hand.append(shuffledcards.pop())
    #     #         self.cards_out = card_values[:]
    #     #     for card in self.hand:
    #     #         del self.cards_out[self.cards_out.index(card)]
    #     for card in range(5):
    #         self.hand.append(shuffledcards.pop())
    #         self.cards_out = card_values[:]
    #     for card in self.hand:
    #         del self.cards_out[self.cards_out.index(card)]

    #     self.handbu = self.hand[:]
    #     self.cards_outbu=self.cards_out[:]

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
        if replay == 2:
            self.cardvalues = self.handbu[:]
        else:
            for card in self.hand:
                value = calc_card_point_value(trump_local, card)
                self.cardvalues.append(value)
        return self.cardvalues

    def calc_handvalue(self, trump_local, topcard, is_first_bidding_round):
        'Totals up hand value based on particular assumption of trump.'
        self.handvalue = 0
        trial_hand = self.hand[:]
        if is_first_bidding_round and self.isDealer:
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
            if not(card[0] == trump_local) and not card == LB_local:
                discardvalues[count] = (card[1] - 4.5) / pow(suitcounts[card[0]], 3)  # formula computes value of all non-trump card values by subtracting 4.5 from positional value,  then dividing by the cube of all cards in that suit.
            count += 1
        if len(trial_hand) == 6:
            del trial_hand[discardvalues.index(min(discardvalues))]
        for card in trial_hand:
            self.handvalue += calc_card_point_value(trump_local, card)
            if card[1] < 5 and card[1] > 0:
                self.handvalue -= 1  # reduces value of 10 through King for bidding purposes
        trumpvoid = 1
        if suitcounts[trump_local] > 0:
            trumpvoid = 0
        if not(trumpvoid):
            for suit in range(0, 4):
                if suitcounts[suit] == 0 and not(suit == trump_local): self.handvalue += 6
        if is_first_bidding_round:
            if self.partner.number == dealer_num: #Extra points for adding up-card to hand or to partner's hand.
                self.handvalue += (calc_card_point_value(trump_local, topcard) +3)
            if self.opposingteam == dealer.opposingteam: self.handvalue -= (calc_card_point_value(trump_local, topcard) + 3) #Negative points for adding up-card to opposing team's hand,  plus extra penalty (3) for possibility they'll create a void.
        return (self.handvalue)

    def hand_owner_label(self):
        return "\n{0}'s hand:".format(self.name)

    def showhand(self, trump_local, is_first_bidding_round):
        print self.hand_owner_label()

        self.hand.sort(key=lambda card: card[1])  # sort by position
        self.hand.sort(key=lambda card: card[0])  # sort by suit
        LB_local = (999, 999)
        if is_first_bidding_round and trump_local > -1:
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
                    # removes trump cards from self.hand
                    del self.hand[self.hand.index(card)]
            trumpcardvalues = []
            trumpcards2 = trumpcards[:]
            for card in trumpcards:
                trumpcardvalues.append(calc_card_point_value(trump_local, card)) #calculates values for trump cards

            def findkey(tup):
                """ function returns value of trump card by matching position
                    of the card tuple (suit,  position) in an unchanging master
                    list of trump cards
                """
                return trumpcardvalues[trumpcards2.index(tup)]  #

            trumpcards.sort(key=findkey)  # sorts trump cards according to their value
            for card in self.hand:
                trumpcards.append(card)  # re-attaches cards from rest of hand to trump cards
            self.hand = trumpcards[:]  # assigns new values to self.hand from foregoing
        if self.hand[0] == LB_local:
            currentsuit = trump
        else:
            currentsuit = self.hand[0][0]
        print (suitlabels[currentsuit]+":"),
        for card in self.hand:
            if card == LB_local:
                if not card == self.hand[0]: print(", "),  #, end = ''
                print("Jack of "+suitlabels[card[0]]+" [left bauer]"),  #, end = ""
            elif card[0] == currentsuit:
                if not card == self.hand[0]: print (", "),  #, end = ''
                print(positionlabels[card[1]]+((" of "+suitlabels[card[0]]+" [left bauer]")*(card == LB_local))),  #, end = ''
            else:
                currentsuit = card[0]
                print("\n"+suitlabels[card[0]]+": "+positionlabels[card[1]]),  #, end = ''
        print("\n")

    def bid(self, bidding_round, player_position, topcard):
        self.handval = 0
        # if self.team == Team1:
        #     lowcutR0 = 36
        #     lowcutR1 = 33
        #     highcutR0 = 49
        #     highcutR1 = 46
        # else:
        #     lowcutR0 = 36
        #     lowcutR1 = 33
        #     highcutR0 = 49
        #     highcutR1 = 46
        lowcutR0 = 36
        lowcutR1 = 33
        highcutR0 = 49
        highcutR1 = 46

        if is_first_bidding_round:
            trump = topcard.suit
            self.handval = self.calc_handvalue(trump, topcard, 0)
            if self.handval > lowcutR0:
                if self.handval > highcutR0:
                    bid_type = 2
                else:
                    bid_type = 1
            else:
                bid_type = 0
        else:
            x = [0, 1, 2, 3]
            del x[topcard.suit]
            y = [0, 0, 0]
            count = 0
            for trump in x:
                y[count] = self.calc_handvalue(trump, topcard, 1)
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
        #picks a card for leading a trick
        lead_card_values = [0]*len(self.hand)
        count = 0
        trumplist = [0, 1, 2, 3]
        trumplist = trumplist[trump_local:]+trumplist[:trump_local]
        LB_local = (trumplist[2], 2)
        for card in self.hand:
            #This section to determine value of leading with trump cards.
            if card[0] == trump_local or card == LB_local:
                if self.partner == bidmaker or self == bidmaker:
                    lead_card_values[count] += 6
                else: lead_card_values[count] -= 4
                higher = 0
                trumps_out = self.getsuit(trump_local, self.cards_out, trump_local)
                for card2 in trumps_out:
                    if calc_card_point_value(trump_local, card) < calc_card_point_value(trump_local, card2): higher += 1
                if higher == 0: lead_card_values[count] += 2 #card is higher than trump cards still out in other players hand (or discard pile)
                lead_card_values[count] -= higher
                lead_card_values[count] += (len(self.getsuit(trump_local, self.hand, trump_local))-1) #trump card value as lead increased by other trump in hand
                lead_card_values[count] -= 2*(sum(self.voids[self.number])) #trump card value as lead descreased by voids in hand (missed opportunity to trump opponents' high off-suit cards)
                count += 1
            #This section to determine value of leading with non-trump cards.
            else:
                lower = 0
                higher = 0
                for card2 in self.getsuit(card[0], self.cards_out, trump_local):
                    if calc_card_point_value(trump_local, card) < calc_card_point_value(trump_local, card2): higher += 1
                    else: lower += 1
                if higher == 0: lead_card_values[count] += 2 #Card is high in suit.
                if (lower-higher) > 1: lead_card_values[count] +=1 #Of cards in same suit that are still out there,  lower cards outnumber higher by more than 1.
                if higher > lower: lead_card_values[count] -= 1 #Of cards in same suit that are still out there,  more are higher than lower.
                if sum(self.voids[self.partner.number])> 0 and self.voids[self.partner.number][trump_local] == 0: lead_card_values[count] += 2 #My partner could trump in.
                if self.voids[self.opposingteam.playerA.number][card[0]] == 1:
                    if self.voids[self.opposingteam.playerA.number][trump_local] == 1:
                        lead_card_values[count] += 1 #player in opposing team cannot beat,  cannot trump
                    else: lead_card_values[count] -= 1 #player in opposing team has void,  could possibly trump
                if self.voids[self.opposingteam.playerB.number][card[0]] == 1:
                    if self.voids[self.opposingteam.playerB.number][trump_local] == 1:
                        lead_card_values[count] += 1 #player in opposing team cannot beat,  cannot trump
                    else: lead_card_values[count] -= 1 #player in opposing team has void,  could possibly trump
                if len(self.getsuit(card[0], self.hand, trump_local)) == 1 and len(self.getsuit(trump_local, self.hand, trump_local))>0: lead_card_values[count] += 1 #could create a void in own hand,  then trump
                count +=1
        leadcard = self.hand[lead_card_values.index(max(lead_card_values))]
        return leadcard # NOTE-If highest value is found in more than one card,  the first card in hand will be chosen.

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
                if Players[currentwinner_num] == self.partner:  # If your partner is winning....
                    partnercard = played_cards[tricksequence.index(self.partner)]
                    for card in self.getsuit(leadsuit_local, self.cards_out, trump_local):
                        if calc_card_point_value(trump_local, card) > calc_card_point_value(trump_local, partnercard): # And there's a within-suit card still out that's higher than partner's.
                            # NOTE: This will sometimes lead to playing a higher card than necessary--if in last position,  will play highest card even when a lower might be sure to win; and if partner is just one step below.
                            if calc_card_point_value(trump_local, highcard) > calc_card_point_value(trump_local, partnercard):
                                return highcard #... and could lose to other in-suit card,  then play my high card,  if it beats partner's.
                    else: return lowcard
                else: # If partner not winning....
                    # NOTE: This will sometimes lead to playing a higher card than necessary.
                    if calc_card_point_value(trump_local, highcard) > max(played_cards_values): return highcard
                    else: return lowcard
            elif trumpcards:
                if Players[currentwinner_num] == self.partner:  # If your partner is winning....
                    partnercard = played_cards[tricksequence.index(self.partner)]
                    for card in self.getsuit(leadsuit_local, self.cards_out, trump_local):
                        if calc_card_point_value(trump_local, card) > calc_card_point_value(trump_local, partnercard):
                            if calc_card_point_value(trump_local, lowtrump) > calc_card_point_value(trump_local, partnercard): return lowtrump #... and could lose to other in-suit card,  then play my lowest trump card,  if it beats partner's.
                            elif calc_card_point_value(trump_local, hightrump) > calc_card_point_value(trump_local, partnercard): return hightrump
                else:
                    if calc_card_point_value(trump_local, lowtrump) > max(played_cards_values):
                        return lowtrump
                    else:
                        if calc_card_point_value(trump_local, hightrump) > max(played_cards_values):
                            return hightrump

            # If this point reached,  cannot win trick. Play lowest card.
            for card in self.hand:
                    follow_card_values.append(calc_card_point_value(trump_local, card))
                    if self.getsuit(card[0], self.hand, trump_local) == 1: follow_card_values[len(follow_card_values)] -= 4
            followcard = self.hand[follow_card_values.index(min(follow_card_values))]
            return followcard

    def play(self, leadsuit_local, trump_local):
        if tricksequence.index(self) == 0:
            play_card = self.lead(trump_local)
        else: play_card = self.follow(leadsuit_local, trump_local)
        del self.hand[self.hand.index(play_card)]
        return play_card

