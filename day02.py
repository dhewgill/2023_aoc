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

def do_d2p1(fpath: str) -> int:
    flines = parse_file(fpath)

    possible = {"red": 12, "green": 13, "blue": 14}

    games = []
    for line in flines:
        # Get game id.
        g_id, rest = line.split(": ")
        g_id = int(g_id.split()[-1])
        game_is_possible = True

        # Get the game records.
        records = rest.split("; ")
        for r in records:
            tally = {k: 0 for k in possible}
            draw = r.split(", ")
            for d in draw:
                num, color = d.split()
                tally[color] += int(num)

            if any(v > possible[k] for k, v in tally.items()):
                game_is_possible = False
                break

        if game_is_possible:
            games.append(g_id)

    return sum(games)


def do_d2p2(fpath: str) -> int:
    flines = parse_file(fpath)

    games = []
    for line in flines:
        # Get game id.
        g_id, rest = line.split(": ")
        g_id = int(g_id.split()[-1])

        tallies = {"red": [], "green": [], "blue": []}

        # Get the game records.
        records = rest.split("; ")
        for r in records:
            draw = r.split(", ")
            for d in draw:
                num, color = d.split()
                tallies[color].append(int(num))
        game_pwr = 1
        for v in tallies.values():
            game_pwr *= max(v)
        games.append(game_pwr)

    return sum(games)


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
