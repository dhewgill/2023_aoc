#!/usr/bin/env python
"""
Haunted Wasteland
"""
import argparse
import logging
import sys

from common import parse_file

# ####################################
# --------------  Main  --------------
P1_DATFILE = r".\data\d8p1_eg1.dat"
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
    _ = do_d8p1(P1_DATFILE)
    print(f"d8p1 = {None}")

    # Part 2.
    _ = do_d8p2(P2_DATFILE)
    print(f"d8p2 = {None}")

    print("\n\nEnd")


# ####################################
# --------------  Util  --------------
def do_d8p1(fpath: str) -> int:
    flines = parse_file(fpath)

    return -1


def do_d8p2(fpath: str) -> int:
    flines = parse_file(fpath)

    return -1


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
