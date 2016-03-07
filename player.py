"""Player class."""

from bid import Bid
from deck import SUITS
from deck import Deck
from deck import limit_to_suit
from deck import suits_trump_first

NUM_PLAYERS = 4


class Player(object):

    lowcutR0 = 36
    lowcutR1 = 33
    highcutR0 = 49
    highcutR1 = 46

    def __init__(self, name, isDealer=False):
        self.name = name
        self.partner = None
        # For each player, count occurences of each suit, I think:
        self.voids = []
        self.hand = []
        self.handvalue = 0
        self.handbu = []
        self.isDealer = isDealer
        self.reset_voids()
        self.cards_out = Deck()  # all players count cards

    def __repr__(self):
        partner = "(no partner)"
        if self.partner is not None:
            partner = self.partner.name

        return "<{0} {1}, partner of {2}>".format(
            self.__class__.__name__, self.name, partner
        )

    def add_card(self, card):
        self.hand.append(card)
        self.updatecards_out(card)

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

    def getsuit(self, suit, cards, trump):
        """ Return just the cards in the specified suit, including
            the left bauer if the suit is the trump suit.
        """
        return [
            card for card in cards
            if card.is_same_suit(suit=suit, trump=trump)
        ]

    def ordered_up(self, topcard):
        """ Find the card that hurts the hand the least and ditch it.
            XXX Does the card that's discarded get shown to other players?
        """
        handbackup = self.hand[:]
        discardvalues = []
        for discard in range(6):
            self.hand = handbackup[:]
            del(self.hand[discard])
            discardvalues.append(self.calc_handvalue(topcard.trump, 0))
        self.hand = handbackup
        del(self.hand[discardvalues.index(max(discardvalues))])

    def setpartner(self, partner):
        self.partner = partner

    def setteam(self, team):
        self.team = team
    # If player knows, based on played cards and own hand,
    # there's a void in a suit, this is registered as a void
    # for all players, only known to player.
    def check_for_exhausted_suits(self, trump):
        for suit in SUITS:
            if len(limit_to_suit(self.cards_unseen, suit, trump)) == 0:
                for p2 in self.players:
                    self.learns_void(p2, suit)

    def setopposingteam(self, team):
        self.opposingteam = team

    def updatecards_out(self, card):
        self.cards_out.remove(card)

    def getcardvalues(self, trump):
        self.cardvalues = []
        if replay == 2:
            self.cardvalues = self.handbu[:]
        else:
            for card in self.hand:
                self.cardvalues.append(card.value(trump))
        return self.cardvalues

    def calc_handvalue(self, trump, topcard=None, is_first_bidding_round=False):
        'Totals up hand value based on particular assumption of trump.'
        self.handvalue = 0
        trial_hand = self.hand[:]
        if is_first_bidding_round and self.isDealer:
            trial_hand.append(topcard)
        suitcounts = self._suit_counter(trump)
        for card in trial_hand:
            suitcounts[card.effective_suit(trump)] += 1
        # Calculate temporary card values.
        discardvalues = [9] * len(trial_hand)
        count = 0
        for card in trial_hand:
            if not card.effective_suit(trump) == trump:
                # formula computes value of all non-trump card values by
                # subtracting 4.5 from positional value,
                # then dividing by the cube of all cards in that suit.
                discardvalues[count] = (card.raw_value - 4.5) / pow(suitcounts[card.suit], 3)
            count += 1
        if len(trial_hand) == 6:
            del trial_hand[discardvalues.index(min(discardvalues))]
        for card in trial_hand:
            self.handvalue += card.value(trump)
            if card.raw_value < 5 and card.raw_value > 0:
                # reduces value of 10 through King for bidding purposes
                self.handvalue -= 1
        has_trumps = suitcounts[trump] > 0
        if has_trumps:
            for suit in SUITS:
                if suitcounts[suit] == 0 and not suit == trump:
                    self.handvalue += 6
        if is_first_bidding_round:
            if self.partner.isDealer:
                # Extra points for adding up-card to hand or to partner's hand.
                self.handvalue += topcard.value(trump) + 3
            # Negative points for adding up-card to opposing team's hand,
            # plus extra penalty (3) for possibility they'll create a void.
            # XXX This seems to just check if my partner is the dealer again?
            # if self.opposingteam == dealer.opposingteam:
            #     self.handvalue -= topcard.value(trump) + 3)

        return self.handvalue

    def hand_owner_label(self):
        return "\n{0}'s hand:".format(self.name)

    def showhand(self, trump, is_first_bidding_round):
        print(self.hand_owner_label())

        self.hand.sort(key=lambda card: card[1])  # sort by position
        self.hand.sort(key=lambda card: card[0])  # sort by suit
        left_bauer_local = (999, 999)
        if is_first_bidding_round and trump > -1:
            trumpcards = []
            for card in self.hand:
                if card.effective_suit(trump) == trump:
                    trumpcards.append(card)
            selfhandmatch = self.hand[:]
            for card in selfhandmatch:
                if card in trumpcards:
                    # removes trump cards from self.hand
                    del self.hand[self.hand.index(card)]
            trumpcardvalues = []
            trumpcards2 = trumpcards[:]
            for card in trumpcards:
                trumpcardvalues.append(card.value(trump))

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
        if self.hand[0] == left_bauer_local:
            currentsuit = trump
        else:
            currentsuit = self.hand[0][0]
        print (suitlabels[currentsuit] + ":"),
        for card in self.hand:
            if card == left_bauer_local:
                if not card == self.hand[0]:
                    print(", "),  #, end = ''
                print("Jack of " + suitlabels[card[0]] + " [left bauer]"),  #, end = ""
            elif card[0] == currentsuit:
                if not card == self.hand[0]:
                    print (", "),  #, end = ''
                print(positionlabels[card[1]] + ((" of " + suitlabels[card[0]] + " [left bauer]") * (card == left_bauer_local))),  #, end = ''
            else:
                currentsuit = card[0]
                print("\n" + suitlabels[card[0]] + ": " + positionlabels[card[1]]),  #, end = ''
        print("\n")

    def learns_void(self, player, suit):
        """Learn about a void suit in another player's hand."""
        self.voids[player.number][suit] = 1

    def callPass(self):
        return Bid(self, Bid.PASS)

    def callBid(self, trump):
        return Bid(self, Bid.BID, trump)

    def callAlone(self, trump):
        return Bid(self, Bid.ALONE, trump)

    def bid_first_round(self, player_position, topcard):
        trump = topcard.suit
        handvalue = self.calc_handvalue(
            trump=trump,
            topcard=topcard,
            is_first_bidding_round=True
        )
        bid = self._bid_for_handvalue(handvalue)

        return bid

    def bid_second_round(self, player_position, topcard):
        possible_trumps = [suit for suit in SUITS if suit != topcard.suit]
        trump_scores = {}
        for trump in possible_trumps:
            trump_scores[trump] = self.calc_handvalue(
                trump=trump,
                topcard=topcard,
                is_first_bidding_round=False
            )
        trump = max(trump_scores.keys(), key=(lambda k: trump_scores[k]))
        handvalue = trump_scores[trump]
        bid = self._bid_for_handvalue(handvalue)

        return bid

    def _bid_for_handvalue(self, handvalue, trump=None):
        if handvalue > self.highcutR1:
            bid = self.callAlone(trump)
        elif handvalue > self.lowcutR1:
            bid = self.callBid(trump)
        else:
            bid = self.callPass()

        return bid

    def lead(self, bidmaker, trump):
        # picks a card for leading a trick
        lead_card_values = [0] * len(self.hand)
        count = 0
        for card in self.hand:
            # This section to determine value of leading with trump cards.
            if card.effective_suit(trump) == trump:
                if self.partner == bidmaker or self == bidmaker:
                    lead_card_values[count] += 6
                else:
                    lead_card_values[count] -= 4
                higher = 0
                trumps_out = limit_to_suit(self.cards_unseen, trump, trump)
                for card2 in trumps_out:
                    if card.value(trump) < card2.value(trump):
                        higher += 1
                if higher == 0:
                    # card is higher than trump cards still out in other
                    # players hand (or discard pile)
                    lead_card_values[count] += 2
                lead_card_values[count] -= higher
                # trump card value as lead increased by other trump in hand
                lead_card_values[count] += (
                    len(limit_to_suit(self.hand, trump, trump)) - 1
                )
                # trump card value as lead descreased by voids in hand
                # (missed opportunity to trump opponents' high off-suit cards)
                lead_card_values[count] -= 2 * self.known_void_suit_count(self)
                count += 1
            # This section to determine value of leading with non-trump cards.
            else:
                lower = 0
                higher = 0
                for card2 in limit_to_suit(self.cards_unseen, card.suit, trump):
                    if card.value(trump) < card2.value(trump):
                        higher += 1
                    else:
                        lower += 1
                if higher == 0:
                    lead_card_values[count] += 2  # Card is high in suit.
                if (lower - higher) > 1:
                    lead_card_values[count] += 1  # Of cards in same suit that are still out there,  lower cards outnumber higher by more than 1.
                if higher > lower:
                    lead_card_values[count] -= 1  # Of cards in same suit that are still out there,  more are higher than lower.
                if self.known_to_have_voids(self.partner) and not self.known_to_be_void_in(self.partner, trump):
                    lead_card_values[count] += 2  # My partner could trump in.
                for opponent in self.opposingteam:
                    if self.known_to_be_void_in(opponent, card.suit):
                        if self.known_to_be_void_in(opponent, trump):
                            # player in opposing team cannot beat,  cannot trump
                            lead_card_values[count] += 1
                        else:
                            # player in opposing team has void, and could possibly trump
                            lead_card_values[count] -= 1

                if len(limit_to_suit(self.hand, card.suit, trump)) == 1 \
                   and len(limit_to_suit(self.hand, trump, trump)) > 0:
                    lead_card_values[count] += 1  # could create a void in own hand,  then trump
                count += 1
        leadcard = self.hand[lead_card_values.index(max(lead_card_values))]
        return leadcard  # NOTE-If highest value is found in more than one card,  the first card in hand will be chosen.

    def follow(self, current_winner, leadsuit, trump, tricksequence, played_cards):
        """ We do want to track the winner, not the leader.... Must fix this."""
        follow_card_values = []
        played_cards_values = [card.value(trump) for card in played_cards]
        validcards = limit_to_suit(self.hand, leadsuit, trump)
        trumpcards = limit_to_suit(self.hand, trump, trump)
        validcardvalues = []
        trumpcardvalues = []
        for validcard in validcards:
                validcardvalues.append(validcard.value(trump))
        for trumpcard in trumpcards:
                trumpcardvalues.append(trumpcard.value(trump))
        if validcards:
            lowcard = validcards[validcardvalues.index(min(validcardvalues))]
            highcard = validcards[validcardvalues.index(max(validcardvalues))]
        if trumpcards:
            lowtrump = trumpcards[trumpcardvalues.index(min(trumpcardvalues))]
            hightrump = trumpcards[trumpcardvalues.index(max(trumpcardvalues))]
        if validcards:
            if current_winner == self.partner:  # If your partner is winning....
                partnercard = played_cards[tricksequence.index(self.partner)]
                for card in limit_to_suit(self.cards_unseen, leadsuit, trump):
                    if card.value(trump) > partnercard.value(trump): # And there's a within-suit card still out that's higher than partner's.
                        # NOTE: This will sometimes lead to playing a higher card than necessary--if in last position,  will play highest card even when a lower might be sure to win; and if partner is just one step below.
                        if highcard.value(trump) > partnercard.value(trump):
                            return highcard  # ... and could lose to other in-suit card,  then play my high card,  if it beats partner's.
                else:
                    return lowcard
            else:  # If partner not winning....
                # NOTE: This will sometimes lead to playing a higher card than necessary.
                if highcard.value(trump) > max(played_cards_values):
                    return highcard
                else:
                    return lowcard
        elif trumpcards:
            if current_winner == self.partner:  # If your partner is winning....
                partnercard = played_cards[tricksequence.index(self.partner)]
                for card in limit_to_suit(self.cards_unseen, leadsuit, trump):
                    if card.value(trump) > partnercard.value(trump):
                        if lowtrump.value(trump) > partnercard.value(trump):
                            return lowtrump  # ... and could lose to other in-suit card,  then play my lowest trump card,  if it beats partner's.
                        elif hightrump.value(trump) > partnercard.value(trump):
                            return hightrump
            else:
                if lowtrump.value(trump) > max(played_cards_values):
                    return lowtrump
                else:
                    if hightrump.value(trump) > max(played_cards_values):
                        return hightrump

        # If this point reached,  cannot win trick. Play lowest card.
        for card in self.hand:
            follow_card_values.append(card.value(trump))
            if len(limit_to_suit(self.hand, card.suit, trump)) == 1:
                follow_card_values[-1] -= 4
        followcard = self.hand[follow_card_values.index(min(follow_card_values))]
        return followcard

    def play(self, current_winner, leadsuit, trump, tricksequence, played_cards, played_card_values):
        if tricksequence.index(self) == 0:
            play_card = self.lead(trump=trump, bidmaker=self)
        else:
            play_card = self.follow(
                current_winner, leadsuit, trump, tricksequence, played_cards, played_card_values
            )
        del self.hand[self.hand.index(play_card)]
        return play_card

    def reset_voids(self):
        self.voids = [self._suit_counter() for i in range(NUM_PLAYERS)]

    def known_void_suit_count(self, player):
        """ How many suits is another player known to be void in? """
        voids_for_player = self.voids[player.number]

        return sum(voids_for_player.values())

    def known_to_have_voids(self, player):
        """ Return true if player is known to have *any* void suits """
        return self.known_void_suit_count(player) > 0

    def known_to_be_void_in(self, player, suit):
        """ Does this player know that another player is void in a given suit?
        """
        return self.voids[player.number][suit] > 0

    def _suit_counter(self, trump=None):
        return {suit: 0 for suit in suits_trump_first(trump)}
