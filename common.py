#!/usr/bin/env python
from functools import lru_cache, reduce
import itertools
import math


@lru_cache(maxsize=2)
def parse_file(f, strip_eol=True):
    with open(f, mode='r') as fd:
        raw_fl = fd.readlines()
    if strip_eol:
        flines = tuple(l.replace("\n", "") for l in raw_fl)
    else:
        flines = tuple(raw_fl)
    return flines

def grouper(iterable, n, *, incomplete='fill', fillvalue=None):
    """
    Collect data into non-overlapping fixed-length chunks or blocks
    Straight from itertools recipes:
    https://docs.python.org/3/library/itertools.html#itertools-recipes
    """
    # grouper('ABCDEFG', 3, fillvalue='x') --> ABC DEF Gxx
    # grouper('ABCDEFG', 3, incomplete='strict') --> ABC DEF ValueError
    # grouper('ABCDEFG', 3, incomplete='ignore') --> ABC DEF
    args = [iter(iterable)] * n
    if incomplete == 'fill':
        return itertools.zip_longest(*args, fillvalue=fillvalue)
    if incomplete == 'strict':
        return zip(*args, strict=True)
    if incomplete == 'ignore':
        return zip(*args)
    else:
        raise ValueError('Expected fill, strict, or ignore')

def lcm(seq):
    # math.lcm is only available in Python 3.9+
    try:
        return math.lcm(*seq)
    except AttributeError:
        return reduce(lambda x,y:(x*y)//math.gcd(x,y), seq)
