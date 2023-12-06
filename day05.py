#!/usr/bin/env python
"""
If You Give A Seed A Fertilizer
"""
import argparse
import logging
import sys

from common import parse_file

# ####################################
# --------------  Main  --------------
P1_DATFILE = r".\data\d5p1.dat"
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
    loc = do_d5p1(P1_DATFILE)
    print(f"d5p1 = {loc}") # 157211394

    # Part 2.
    loc2 = do_d5p2(P2_DATFILE)
    print(f"d5p2 = {loc2}")

    print("\n\nEnd")


# ####################################
# --------------  Util  --------------
def parse_seeds(almanac: list) -> tuple:
    seeds = None
    for line in almanac:
        if "seeds:" in line:
            _, seed_nums = line.split(": ")
            seeds = tuple(int(s) for s in seed_nums.split())
            break

    return seeds


def parse_mappings(almanac: str) -> dict:
    """
    destination, source, range
    """
    mappings = {}
    current_key = None
    last_key = None
    this_entry = {}
    for line in almanac:
        if "map:" in line:
            current_key = line.split()[0]
            this_entry = {"dst": [], "src": [], "rng": [], "nxt": None}

        elif line == "":
            # End of parsing for the current key.
            if this_entry != {}:
                if last_key is not None:
                    mappings[last_key]["nxt"] = current_key
                mappings[current_key] = this_entry
                last_key = current_key
                current_key = None

        else:
            if current_key is not None:
                # Parse numbers.
                dst, src, rng = (int(v) for v in line.split())
                this_entry["dst"].append(int(dst))
                this_entry["src"].append(int(src))
                this_entry["rng"].append(int(rng))

    return mappings


def do_d5p1(fpath: str) -> int:
    flines = parse_file(fpath)

    seeds = parse_seeds(flines)
    #print(seeds)
    mappings = parse_mappings(flines)
    #print(mappings)

    seed_locs = []
    for seed in seeds:
        last_map = seed

        for m_name, m in mappings.items():
            for dst, src, rng in zip(m["dst"], m["src"], m["rng"]):
                this_map = last_map # Default case; straight mapping.
                if src <= last_map < (src + rng):
                    this_map = last_map - src + dst
                    break
            last_map = this_map
        seed_locs.append(last_map)

    #print(seed_locs)
    return min(seed_locs)


def do_d5p2(fpath: str) -> int:
    flines = parse_file(fpath)

    seeds = parse_seeds(flines)
    #print(seeds)
    mappings = parse_mappings(flines)
    #print(mappings)

    seed_rngs = [(s, sr) for s, sr in zip(seeds[::2], seeds[1::2])]
    print(seed_rngs)
    seed_locs = []
    for seed_s, seed_rng in seed_rngs:
        for seed in range(seed_s, seed_s + seed_rng): # <- Horribly inefficient, and never finishes.
            last_map = seed

            for m_name, m in mappings.items():
                for dst, src, rng in zip(m["dst"], m["src"], m["rng"]):
                    this_map = last_map # Default case; straight mapping.
                    if src <= last_map < (src + rng):
                        this_map = last_map - src + dst
                        break
                last_map = this_map
            seed_locs.append(last_map)

    print(seed_locs)
    return min(seed_locs)


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
