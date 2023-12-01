#!/usr/bin/env python

import argparse
import logging
import sys

from common import parse_file

# ####################################
# --------------  Main  --------------
P1_DATFILE = None
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


    print("\n\nEnd")


# ####################################
# --------------  Util  --------------


# ####################################
# --------  main() execute  ----------
if __name__ == '__main__':
    sys.exit(main())
