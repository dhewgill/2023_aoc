#!/usr/bin/env python
"""
Trebuchet calibration.
"""
import argparse
import logging
import sys

from common import parse_file

# ####################################
# --------------  Main  --------------
P1_DATFILE = r".\data\d1p1.dat"
P2_DATFILE = None

def main(argv=None):
    if argv is None:
        argv = sys.argv
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--log-lvl", dest="log_lvl", type=str, default="INFO", help="Logging level.")
    args = parser.parse_args()
    log_lvl = args.log_lvl
    
    logging.basicConfig(level=log_lvl)
    
    print("Start\n")

    d1p1_coords = do_d1p1(P1_DATFILE)
    print(f"d1p1 = {d1p1_coords}") # 55172

    print("\n\nEnd")


# ####################################
# --------------  Util  --------------
def get_p1_line_score(input_line: str) -> int:
    digit = ""
    # Find the first digit.
    for c in input_line:
        if c.isdigit():
            digit += c
            break
    
    # Find the last digit.
    for c in input_line[::-1]:
        if c.isdigit():
            digit += c
            break
    
    return int(digit)


def do_d1p1(fpath: str) -> int:
    flines = parse_file(fpath)
    return sum(get_p1_line_score(l) for l in flines)


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
