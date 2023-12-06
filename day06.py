#!/usr/bin/env python
"""
Wait For It
"""
import argparse
import logging
import sys

from common import parse_file

# ####################################
# --------------  Main  --------------
P1_DATFILE = r".\data\d6p1.dat"
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
    margin = do_d6p1(P1_DATFILE)
    print(f"d6p1 = {margin}") # 4811940

    # Part 2.
    do_d6p2(P2_DATFILE)
    print(f"d6p2 = {None}")

    print("\n\nEnd")


# ####################################
# --------------  Util  --------------
def parse_sheet(sheet: list) -> dict:
    parsed = {"times": [], "distances": []}
    for s in sheet:
        if "Time:" in s:
            key = "times"
        else:
            key = "distances"
        for v in s.split()[1:]:
            parsed[key].append(int(v))
    return parsed


def do_d6p1(fpath: str) -> int:
    flines = parse_file(fpath)
    sheet = parse_sheet(flines)
    #print(sheet)

    success_margin = 1
    for t, d in zip(sheet["times"], sheet["distances"]):
        win_count = 0
        for i in range(1, t):
            this_d = i * (t - i)
            #print(f"{i}: {this_d}")
            if this_d > d:
                win_count += 1
        success_margin *= win_count

    return success_margin


def do_d6p2(fpath: str) -> int:
    flines = parse_file(fpath)

    return None


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
