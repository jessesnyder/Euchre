"""Class Bid."""
from deck import SUITS


class Bid(object):
    """ Data object representing a bid.

        'type' could be 'bid', 'pass', or 'alone'
        'trump' is the chosen trump suit

        In practice, the @classmethod constructors should be used
        instead of the standard constructor.
    """
    PASS = 'pass'
    BID = 'bid'
    ALONE = 'alone'

    def __init__(self, player, bidtype, trump=None):
        if bidtype not in (self.PASS, self.BID, self.ALONE):
            raise ValueError("Invalid bid type!")
        if trump is not None and trump not in SUITS:
            raise ValueError("Invalid trump suit!")
        self.player = player
        self.type = bidtype
        self.trump = trump

    # Alternate constructors:
    @classmethod
    def a_pass(cls, player):
        return cls(player, cls.PASS)

    @classmethod
    def a_bid(cls, player, trump):
        return cls(player, cls.BID, trump)

    @classmethod
    def go_alone(cls, player, trump):
        return cls(player, cls.ALONE, trump)

    # Instance methods:
    @property
    def is_pass(self):
        return self.type == self.PASS

    @property
    def is_alone(self):
        return self.type == self.ALONE
