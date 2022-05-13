#!/usr/bin/env python3
import sys
import re

REQUIRED_YEARS = [2010, 2016]

for line in sys.stdin:
    if line.lstrip(' ').startswith('<row'):
        date_re = re.search('CreationDate=', line)
        if date_re:
            year = int(line[date_re.end()+1:date_re.end()+5])
            if year in REQUIRED_YEARS:
                tags_re = re.search('Tags=', line)
                if tags_re:
                    tags = line[tags_re.end():].split('"', maxsplit=2)[1]
                    for tag in tags.split('&lt;'):
                        if tag:
                            print(year, tag[:-4], 1, sep='\t')
