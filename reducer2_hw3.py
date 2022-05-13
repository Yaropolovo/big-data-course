#!/usr/bin/env python3
import sys

rows_left = {'2010': 10, '2016': 10}

for line in sys.stdin:
    year, counts, tag = line.strip().split("\t")
    if int(counts) > 0:
        if rows_left[year] > 0:
            print(year, tag, counts, sep="\t")
            rows_left[year] = rows_left[year] - 1
