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
P1_DATFILE = r".\data\d8p1.dat"
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
    steps = do_d8p1(P1_DATFILE)
    print(f"d8p1 = {steps}") # 13207

    # Part 2.
    _ = do_d8p2(P2_DATFILE)
    print(f"d8p2 = {None}")

    print("\n\nEnd")


# ####################################
# --------------  Util  --------------
def parse_network(network: list) -> dict:
    net_map = {}
    for n in network:
        n_dict = {"L": None, "R": None}
        node, next_nodes = n.split(" = ")
        l, r = next_nodes.split(", ")
        n_dict["L"] = l.strip("(")
        n_dict["R"] = r.strip(")")
        net_map[node] = n_dict

    return net_map

def do_d8p1(fpath: str) -> int:
    flines = parse_file(fpath)
    instructions = flines[0]

    the_map = parse_network(flines[2:])
    #print(the_map)

    end_node = "ZZZ"
    steps = 1
    node = "AAA"
    found = False
    while not found:
        for d in instructions:
            next_node = the_map[node][d]
            if next_node == end_node:
                found = True
                break
            node = next_node
            steps += 1

    return steps


def do_d8p2(fpath: str) -> int:
    flines = parse_file(fpath)

    return -1


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
