from collections import namedtuple
from enum import Enum
from typing import Sequence

Suit = Enum("Suit", list("SHDC"))
Rank = Enum("Rank", list("AKQJT98765432"))
Card = namedtuple("Card", ["suit", "rank"])

HCP = {Rank.A: 4, Rank.K: 3, Rank.Q: 2, Rank.J: 1}
SSP = {2: 1, 1: 2, 0: 3}  # cards in a suit -> short suit points

Suit_val = {Suit.S: 0, Suit.H: 1, Suit.D: 2, Suit.C: 3}
Rank_val = {Rank.A: 0, Rank.K: 1, Rank.Q: 2, Rank.J: 3,
            Rank.T: 4, Rank['9']: 5, Rank['8']: 6, Rank['7']: 7,
            Rank['6']: 8, Rank['5']: 9, Rank['4']: 10, Rank['3']: 11,
            Rank['2']: 12}


def card_value(card: Card) -> int:
    return Rank_val[card.rank] + Suit_val[card.suit] * 100


class BridgeHand:
    def __init__(self, cards: Sequence[Card]):
        """
        Process and store the sequence of Card objects passed in input.
        Raise TypeError if not a sequence
        Raise ValueError if any element of the sequence is not an instance
        of Card, or if the number of elements is not 13
        """
        if not isinstance(cards, Sequence):
            raise TypeError('Cards must be passed as a sequence')
        if len(cards) != 13 or not all(isinstance(card, Card) for card in cards):
            raise ValueError('There must be exactly 13 cards in a hand')
        self.hand = sorted(cards, key=card_value)

    def __str__(self) -> str:
        """
        Return a string representing this hand, in the following format:
        "S:AK3 H:T987 D:KJ98 C:QJ"
        List the suits in SHDC order, and the cards within each suit in
        AKQJT..2 order.
        Separate the suit symbol from its cards with a colon, and
        the suits with a single space.
        Note that a "10" should be represented with a capital 'T'
        """
        result = []
        for suit in Suit:
            card_set = ''.join(card.rank.name for card in self.hand if card.suit == suit)
            if len(card_set):
                result.append(f'{suit.name}:{card_set}')
        return ' '.join(result)

    @property
    def hcp(self) -> int:
        """ Return the number of high card points contained in this hand """
        return sum(HCP[card.rank] for card in self.hand if card.rank in HCP)

    @property
    def doubletons(self) -> int:
        """ Return the number of doubletons contained in this hand """
        s = self.__str__().split()
        return sum(len(sub) == 4 for sub in s)

    @property
    def singletons(self) -> int:
        """ Return the number of singletons contained in this hand """
        s = self.__str__().split()
        return sum(len(sub) == 3 for sub in s)

    @property
    def voids(self) -> int:
        """ Return the number of voids (missing suits) contained in
            this hand
        """
        s = self.__str__().split()
        return 4 - len(s)

    @property
    def ssp(self) -> int:
        """ Return the number of short suit points in this hand.
            Doubletons are worth one point, singletons two points,
            voids 3 points
        """
        return self.doubletons + self.singletons * 2 + self.voids * 3

    @property
    def total_points(self) -> int:
        """ Return the total points (hcp and ssp) contained in this hand """
        return self.hcp + self.ssp

    @property
    def ltc(self) -> int:
        """ Return the losing trick count for this hand - see bite description
            for the procedure
        """
        s = [sub[:5] for sub in self.__str__().split()]
        c = 0
        for sub in s:
            _, cards = sub.split(':')
            #     - a void = 0 losing tricks.
            # Automagically gone anyway
            #     - a singleton other than an A = 1 losing trick.
            if len(cards) == 1:
                c += 1 if cards != 'A' else 0
            #     - a doubleton AK = 0; Ax or Kx = 1; Qx or xx = 2 losing tricks.
            elif len(cards) == 2:
                c += 0 if cards == 'AK' else 1 if cards[0] in 'AK' else 2
            #     - a three card suit AKQ = 0; AKx, AQx or KQx = 1 losing trick.
            #     - a three card suit Axx, Kxx or Qxx = 2; xxx = 3 losing tricks.
            else:
                c += 0 if cards == 'AKQ' else 1 if cards[:2] in ['AK', 'AQ', 'KQ'] else 2 if cards[0] in 'AKQ' else 3
        return c
