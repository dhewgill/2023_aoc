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
P2_DATFILE = P1_DATFILE #r".\data\d1p2_eg.dat"

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
    d1p1_coords = do_d1p1(P1_DATFILE)
    print(f"d1p1 = {d1p1_coords}") # 55172

    # Part 2.
    d1p2_coords = do_d1p2(P2_DATFILE)
    print(f"d1p2 = {d1p2_coords}") # 54925

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


def get_p2_line_score(input_line: str) -> int:
    str_tokens = ("one", "two", "three", "four", "five", "six", "seven", "eight", "nine",)
    int_tokens = ("1", "2", "3", "4", "5", "6", "7", "8", "9",)

    str_tokens_map = {t: f"{i}" for i, t in enumerate(str_tokens, 1)}

    left_tok = None
    left_indx = len(input_line)

    right_tok = None
    right_indx = -1

    for tok in str_tokens + int_tokens:
        li = input_line.find(tok)
        if li > -1:
            if li < left_indx:
                left_indx = li
                left_tok = tok

        ri = input_line.rfind(tok)
        if ri > -1:
            if ri > right_indx:
                right_indx = ri
                right_tok = tok

    digit = ""
    for tok in (left_tok, right_tok):
        if tok.isdigit():
            digit += tok
        else:
            digit += str_tokens_map[tok]

    return int(digit)


def do_d1p2(fpath: str) -> int:
    flines = parse_file(fpath)
    return sum(get_p2_line_score(l) for l in flines)


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
