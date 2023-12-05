#!/usr/bin/env python
"""
Scratchcards
"""
import argparse
import logging
import sys

from common import parse_file

# ####################################
# --------------  Main  --------------
P1_DATFILE = r".\data\d4p1.dat"
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
    card_points = do_d4p1(P1_DATFILE)
    print(f"d4p1 = {card_points}") # 26443

    # Part 2.
    num_cards = do_d4p2(P2_DATFILE)
    print(f"d4p2 = {num_cards}") # 6284877

    print("\n\nEnd")


# ####################################
# --------------  Util  --------------
def parse_cards(card_pile: list) -> dict:
    """
    Parse cards into dicts of
        {card_num: <int>, win_nums: <tuple>, my_nums: <tuple>}
    """
    for card in card_pile:
        this_card = {"card_num": None, "win_nums": None, "my_nums": None}
        # Get card num.
        card_num, rest = card.split(":")
        this_card["card_num"] = int(card_num.replace("Card ", ""))

        # Split the rest of the card data into winning numbers and my numbers.
        wins, mine = rest.split("|")

        # Get winning numbers.
        this_card["win_nums"] = tuple(int(v) for v in wins.split())

        # Get my numbers.
        this_card["my_nums"] = tuple(int(v) for v in mine.split())

        yield this_card


def do_d4p1(fpath: str) -> int:
    flines = parse_file(fpath)

    total_points = 0
    for card in parse_cards(flines):
        wins = set(card["my_nums"]) & set(card["win_nums"])
        if len(wins) != 0:
            points = 2**(len(wins) - 1)
            total_points += points
        #print(f"Card {card['card_num']}: {points}, {len(wins)}")

    return total_points


def do_d4p2(fpath: str) -> int:
    flines = parse_file(fpath)

    card_tally = {}
    for card in parse_cards(flines):
        card_num = card["card_num"]
        wins = len(set(card["my_nums"]) & set(card["win_nums"]))

        if card_tally.get(card_num) is None:
            card_tally[card_num] = 1
        else:
            card_tally[card_num] += 1

        for _ in range(card_tally.get(card_num, 1)):
            for i in range(card_num + 1, card_num + wins + 1):
                # Assumes cards are numbered consecutively!
                if card_tally.get(i) is None:
                    card_tally[i] = 1
                else:
                    card_tally[i] += 1

    return sum(w for w in card_tally.values())


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
