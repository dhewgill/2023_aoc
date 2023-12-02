#!/usr/bin/env python
"""
Cube Conundrum.
"""
import argparse
import logging
import sys

from common import parse_file

# ####################################
# --------------  Main  --------------
P1_DATFILE = r".\data\d2p1.dat"
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
    possible_id = do_d2p1(P1_DATFILE)
    print(f"d2p1 = {possible_id}") # 2416

    # Part 2.
    game_power = do_d2p2(P2_DATFILE)
    print(f"d1p2 = {game_power}") # 63307

    print("\n\nEnd")


# ####################################
# --------------  Util  --------------
def parse_games(games):
    """
    Parse a game to the form:
    {
        "id": <int>,
        "rounds": [
            {"red": <int>, "green": <int>, "blue": <int>},
            {...},
            ...,
        ],
    }
    """
    for game in games:
        # Get game id.
        g_id, rest = game.split(": ")
        g_id = int(g_id.split()[-1])
        this_game = {"id": g_id, "rounds": []}

        # Get the game rounds.
        rounds = rest.split("; ")
        for r in rounds:
            this_round = {"red": 0, "green": 0, "blue": 0}
            draw = r.split(", ")

            for d in draw:
                num, colour = d.split()
                this_round[colour] = int(num)

            this_game["rounds"].append(this_round)

        yield this_game


def do_d2p1(fpath: str) -> int:
    flines = parse_file(fpath)

    possible = {"red": 12, "green": 13, "blue": 14}
    possible_sum = 0

    for game in parse_games(flines):
        this_sum = game["id"]

        for this_round in game["rounds"]:
            if any(this_round[k] > v for k, v in possible.items()):
                this_sum = 0
                break

        possible_sum += this_sum

    return possible_sum


def do_d2p2(fpath: str) -> int:
    flines = parse_file(fpath)

    power_sum = 0
    for game in parse_games(flines):
        game_pwr = 1

        for colour in game["rounds"][0]:
            game_pwr *= max(v[colour] for v in game["rounds"])

        power_sum += game_pwr

    return power_sum


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
