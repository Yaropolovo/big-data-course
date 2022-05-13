#!/usr/bin/env python3
import sys

current_key = [None, None]
tags_count = 0

for line in sys.stdin:
    year, tag, counts = line.split("\t")
    counts = int(counts)
    if (year, tag) == current_key:
        tags_count += counts
    else:
        if current_key:
            print(current_key[0], current_key[1], tags_count, sep="\t")
        current_key = (year, tag)
        tags_count = counts

if current_key:
    print(current_key[0], current_key[1], tags_count, sep="\t")
