#!/usr/bin/env python
"""
Mirage Maintenance.
"""
import argparse
import logging
import sys

from common import parse_file

# ####################################
# --------------  Main  --------------
P1_DATFILE = r".\data\d9p1.dat"
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
    cumulative_history = do_d9p1(P1_DATFILE)
    print(f"d9p1 = {cumulative_history}") # 1904165718

    # Part 2.
    do_d9p2(P2_DATFILE)
    print(f"d9p2 = {None}")

    print("\n\nEnd")


# ####################################
# --------------  Util  --------------
def get_history(reading: list) -> int:
    new_seq = []
    r_last = reading[0]
    for r in reading[1:]:
        new_seq.append(r - r_last)
        r_last = r
    if all(n==0 for n in new_seq):
        return 0
    return new_seq[-1] + get_history(new_seq)


def do_d9p1(fpath: str) -> int:
    flines = parse_file(fpath)
    cumulative_history = 0
    for l in flines:
        seq = [int(i) for i in l.split()]
        cumulative_history += seq[-1] + get_history(seq)
        print(f"Cumulative History = {cumulative_history}")

    return cumulative_history


def do_d9p2(fpath: str) -> int:
    flines = parse_file(fpath)
    return None


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
