from player import Player


class LivePlayer(Player):

    def hand_owner_label(self):
        return "\nYour hand:"

    def bid(self, is_first_bidding_round, player_position):
        if is_first_bidding_round:
            trump = topcard[0]
            handval = self.calc_handvalue(trump, 0)
            validbids = [0, 1, 2, 88]
            bid_type = 999
            while bid_type not in validbids:
                try:
                    bid_type = input("\nDo you want to bid? (0 = no; 1 = yes; 2 = go alone)")
                except:
                    bid_type = 999
            if bid_type == 88:
                Teams[0].score += 10
                bid_type = 1
            roundinfo = [bid_type, hand, is_first_bidding_round, player_position, handval, trump, topcard, self.hand]
            bidding_data.append(roundinfo)
            self.team.bid = bid_type
            return trump, bid_type
        else:
            self.showhand(-1, 1)
            validbids = [0, 1, 2]
            bid_type = 999
            while bid_type not in validbids:
                try:
                    bid_type = input("\nDo you want to bid? (0 = no; 1 = yes; 2 = go alone)")
                except:
                    bid_type = 999
            if bid_type > 0:
                validtrump = [0, 1, 2, 3]
                trump = 999
                del validtrump[topcard[0]]
                while trump not in validtrump:
                    try:
                        trump = input("Which suit? (hearts = 0,  spades = 1,  diamonds = 2,  clubs = 3)")
                    except:
                        trump = 999
                    if trump == topcard[0]:
                        print("You cannot bid "+suitlabels[topcard[0]]+".")
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
            roundinfo = [bid_type, hand, is_first_bidding_round, player_position, handval, trump, topcard, self.hand]
            bidding_data.append(roundinfo)
            self.team.bid = bid_type
            return trump,  bid_type

    def play(self, leadsuit_local, trump_local):
        self.showhand(trump_local, 0)
        legit = [x+1 for x in range(len(self.hand))]
        pc = 999
        trumplist = [0, 1, 2, 3]
        trumplist = trumplist[trump_local:]+trumplist[:trump_local]
        LB_local = (trumplist[2], 2)
        while pc not in legit:
            try:
                pc = input("Which card? (1 through "+str(len(self.hand))+"): ")
            except:
                pc = 999
            if pc in legit:
                if tricksequence.index(self) > 0:
                    if len(self.getsuit(leadsuit_local, self.hand, trump_local)) > 0:
                        if self.hand[pc - 1] == LB_local and leadsuit == trump_local:
                            pass
                        elif self.hand[pc - 1][0] !=  leadsuit_local and (pc in legit):
                            print("Must follow lead suit.")
                            pc = 99
        play_card = self.hand[pc-1]
        del self.hand[pc-1]
        return play_card
