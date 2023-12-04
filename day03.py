#!/usr/bin/env python
"""
Gear Ratios
"""
import argparse
import logging
import re
import sys

from common import parse_file

# ####################################
# --------------  Main  --------------
P1_DATFILE = r".\data\d3p1.dat"
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
    parts_sum = do_d3p1(P1_DATFILE)
    print(f"d3p1 = {parts_sum}") # 556057

    # Part 2.
    gear_ratio_sums = do_d3p2(P2_DATFILE)
    print(f"d3p2 = {gear_ratio_sums}") # 82824352

    print("\n\nEnd")


# ####################################
# --------------  Util  --------------
def parse_schematic_symbols(raw_schematic: list) -> dict:
    """
    Parse a map into a dictionary of symbol tokens.
    The dict is keyed by the coordinates [as a complex()] and the value is the token.
    All of the tokens are symbols [not digits].
    """
    schematic = {}
    for r, row in enumerate(raw_schematic):
        for c, tok in enumerate(row):
            if (tok != ".") and (not tok.isdigit()):
                schematic[complex(r, c)] = tok

    return schematic


def parse_schematic_digits(raw_schematic: list) -> dict:
    """
    Parse a map into a dictionary of digit tokens.
    The digit tokens are a consecutive digit group, but are added into the dictionary
    as a coordinate for each digit of the group. A unique identifier is added to each digit
    token in order to identify duplicates.
    The dictionary keys are the coordinates of every digit found in the schematic.
    """
    schematic = {}
    for r, row in enumerate(raw_schematic):
        m_iter = re.finditer("[0-9]+", row)
        
        # Unique ID to help identify duplicate numbers.
        uid = 0
        for m in m_iter:
            for c in range(m.start(0), m.end(0)):
                schematic[complex(r, c)] = (m.group(0), uid)
            uid += 1

    return schematic


def is_adjacent_to_symbol(tok_coords: complex, schematic: dict) -> str:
    """
    Is this token adjacent to any symbol in the schematic? If so, return the token,
    else return an empty string.
    A symbol is any token that is not a number.
    The distance is found by complex magnitude - the max adjacent value is complex(1,1).
    """
    adj_distance = abs(complex(1,1))
    is_adjacent = ""
    for tc in schematic:
        if abs(tok_coords - tc) <= adj_distance:
            is_adjacent = schematic[tc]
            break

    return is_adjacent


def get_adjacent_vals(symbol_coord: complex, schematic: dict) -> list:
    adj_distance = abs(complex(1,1))

    adjacents = []
    for pn_coord, pn in schematic.items():
        if abs(pn_coord - symbol_coord) <= adj_distance:
            if not any(pn == p for p in adjacents):
                adjacents.append(pn)

    return adjacents


def do_d3p1(fpath: str) -> int:
    flines = parse_file(fpath)

    symbols = parse_schematic_symbols(flines)
    part_num_sum = 0
    for r, row in enumerate(flines):
        m_iter = re.finditer("[0-9]+", row)
        for m in m_iter:
            for c in range(m.start(0), m.end(0)):
                if is_adjacent_to_symbol(complex(r, c), symbols) != "":
                    part_num_sum += int(m.group(0))
                    break

    return part_num_sum


def do_d3p2(fpath: str) -> int:
    flines = parse_file(fpath)

    symbols = parse_schematic_symbols(flines)
    part_nums = parse_schematic_digits(flines)

    gear_ratio_sum = 0
    for coord, s_val in symbols.items():
        if s_val == "*":
            adjacents = get_adjacent_vals(coord, part_nums)
            print(f"{coord}: {adjacents}")
            if len(adjacents) == 2:
                gear_ratio_sum += int(adjacents[0][0]) * int(adjacents[1][0])

    return gear_ratio_sum


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
