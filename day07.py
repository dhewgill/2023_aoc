#!/usr/bin/env python
"""
Camel Cards
"""
import argparse
from collections import Counter
import logging
import sys

from common import parse_file

# ####################################
# --------------  Main  --------------
P1_DATFILE = r".\data\d7p1.dat"
P2_DATFILE = P1_DATFILE

def main(argv=None):
    if argv is None:
        argv = sys.argv

    parser = argparse.ArgumentParser()
    parser.add_argument("--log-lvl", dest="log_lvl", type=str, default="INFO", help="Logging level.")
    args = parser.parse_args()
    log_lvl = args.log_lvl

    logging.basicConfig(level=log_lvl)

    print("Start\n")

    # Part 1.
    winnings = do_d7p1(P1_DATFILE)
    print(f"d7p1 = {winnings}") # 248113761

    # Part 2.
    with_jokers = do_d7p2(P2_DATFILE)
    print(f"d7p2 = {with_jokers}") # 246285222

    print("\n\nEnd")


# ####################################
# --------------  Util  --------------

CARDS = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
    "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14,
}


class Hand:
    """
    Hierarchy: 5 kind > 4 kind > full > 3 kind > 2 pair > 1 pair > high card
    Tie breaker: first biggest card. 
    """
    hand_ranks = {
        "high": 0, "pair": 1, "pair2": 2, "three": 3, "full": 4, "four": 5, "five": 6,
    }
    card_rank = {
        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
        "T": 10, "J": 11, "Q": 12, "K": 13, "A": 14,
    }

    def __init__(self, hand, bid):
        self.hand = hand
        self.bid = bid
        self.hand_rank = self._classify_hand()

    def _classify_hand(self) -> int:
        this_hand = -1
        card_count = Counter(self.hand)
        most_common = card_count.most_common()

        if most_common[0][1] == 5:
            this_hand = self.hand_ranks["five"]

        elif most_common[0][1] == 4:
            this_hand = self.hand_ranks["four"]

        elif most_common[0][1] == 3:
            if most_common[1][1] == 2:
                this_hand = self.hand_ranks["full"]
            else:
                this_hand = self.hand_ranks["three"]

        elif most_common[0][1] == 2:
            if most_common[1][1] == 2:
                this_hand = self.hand_ranks["pair2"]
            else:
                this_hand = self.hand_ranks["pair"]

        else:
            this_hand = self.hand_ranks["high"]

        return this_hand

    def __gt__(self, other):
        if not isinstance(other, Hand):
            raise ValueError()

        is_gt = False
        if self.hand_rank != other.hand_rank:
            is_gt = self.hand_rank > other.hand_rank

        else:
            for cs, co in zip(self.hand, other.hand):
                #print(f"Compare {cs} to {co}")
                if self.card_rank[cs] != self.card_rank[co]:
                    is_gt = self.card_rank[cs] > self.card_rank[co]
                    break

        return is_gt

    def __repr__(self):
        return f"({self.hand}, {self.bid}, {self.hand_rank})"


class HandJoker(Hand):
    card_rank = {
        "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9,
        "T": 10, "J": 1, "Q": 12, "K": 13, "A": 14,
    }

    def _classify_hand(self) -> int:
        this_hand = -1
        card_count = Counter(self.hand)
        most_common = card_count.most_common()

        if "J" not in self.hand:
            # If there are no jokers then just use the original hand
            # classification method.
            return super()._classify_hand()

        # There are jokers.
        # Jokers add to cards 'most favourably'.
        if most_common[0][1] == 5:
            this_hand = self.hand_ranks["five"]

        elif most_common[0][1] == 4:
            this_hand = self.hand_ranks["five"]

        elif most_common[0][1] == 3:
            if most_common[0][0] == "J":
                if most_common[1][1] == 2:
                    this_hand = self.hand_ranks["five"]
                else:
                    this_hand = self.hand_ranks["four"]
            else:
                if card_count["J"] == 2:
                    this_hand = self.hand_ranks["five"]
                else:
                    this_hand = self.hand_ranks["four"]

        elif most_common[0][1] == 2:
            if card_count["J"] == 1:
                if most_common[1][1] == 2:
                    this_hand = self.hand_ranks["full"]
                else:
                    this_hand = self.hand_ranks["three"]
            else: # J is 2:
                if most_common[1][1] == 2:
                    this_hand = self.hand_ranks["four"]
                else:
                    this_hand = self.hand_ranks["three"]

        else:
            this_hand = self.hand_ranks["pair"]

        return this_hand


def parse_hands(hands: list, hand_type: Hand = Hand) -> list:
    my_hands = []
    for hand in hands:
        h, b = hand.split()
        my_hands.append(hand_type(h, int(b)))

    return my_hands


def do_d7p1(fpath: str):
    flines = parse_file(fpath)
    hands = parse_hands(flines)
    #print(hands)

    sorted_hands = sorted(hands)
    #print(sorted_hands)

    return sum(i * h.bid for i, h in enumerate(sorted_hands, 1))


def do_d7p2(fpath: str):
    flines = parse_file(fpath)
    hands = parse_hands(flines, hand_type = HandJoker)
    #print(hands)

    sorted_hands = sorted(hands)
    #print(sorted_hands)

    return sum(i * h.bid for i, h in enumerate(sorted_hands, 1))


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
