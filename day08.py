#!/usr/bin/env python
"""
Haunted Wasteland
"""
import argparse
import logging
from math import gcd, lcm
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
    ghost_steps = do_d8p2(P2_DATFILE)
    print(f"d8p2 = {ghost_steps}") # 12324145107121

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
    directions = flines[0]

    nodes = parse_network(flines[2:])
    #print(nodes)

    end_node = "ZZZ"
    steps = 1
    node = "AAA"
    found = False
    while not found:
        for d in directions:
            next_node = nodes[node][d]
            if next_node == end_node:
                found = True
                break
            node = next_node
            steps += 1

    return steps


class Node:
    def __init__(self, node_map, start_node):
        self.node_map = node_map
        self.start_node = start_node
        self.current_node = start_node

    def advance(self, direction):
        """
        'direction' is 'L' or 'R'.
        """
        # new_node = self.node_map[self.current_node][direction]
        # print(f"Move from {self.current_node} -> {new_node}")
        self.current_node = self.node_map[self.current_node][direction]

    def traversal_stats(self, directions: str) -> tuple:
        steps_to_first_stop = 1
        period = 1 # Number of steps to return to start.
        steps = 1
        current_node = self.start_node
        while steps_to_first_stop == 1:
            for d in directions:
                current_node = self.node_map[current_node][d]
                if current_node == self.node_map[self.start_node]:
                    period = steps

                elif current_node[-1] == "Z":
                    steps_to_first_stop = steps

                steps += 1

        return (steps_to_first_stop, period)


def do_d8p2(fpath: str) -> int:
    flines = parse_file(fpath)
    directions = flines[0]
    print(f"Number of directions = {len(directions)}")

    nodes = parse_network(flines[2:])
    #print(nodes)

    start_nodes = [Node(nodes, n) for n in nodes if n[-1] == "A"]
    print(f"Found {len(start_nodes)} start nodes.")

    steps = 1

    steps_to_end = {n: 0 for n in start_nodes}
    while start_nodes != []:
        for d in directions:
            for node in start_nodes.copy():
                node.advance(d)
                if node.current_node[-1] == "Z":
                    steps_to_end[node] = steps
                    print(f"Remove node at step {steps} [{steps / len(directions)}]")
                    start_nodes.remove(node)

            if start_nodes == []:
                break

            steps += 1

    return lcm(*steps_to_end.values())


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
