#!/usr/bin/env python3
import sys

for line in sys.stdin:
    year, tag, counts = line.strip().split("\t")
    if year:
        print(year, counts, tag, sep="\t")
