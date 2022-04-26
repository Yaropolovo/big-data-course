#!/usr/bin/env python3
import random
import sys

current_group = ''
current_group_left_ids = random.randint(1,5)

for line in sys.stdin:
    if line:
        modified_id, one = line.split("\t", 1)
        id_intiail = modified_id[5:]

        if id_intiail:
            current_group += id_intiail+','
            current_group_left_ids -= 1

            if current_group_left_ids == 0:
                print(current_group[:-1])
                current_group = ''
                current_group_left_ids = random.randint(1,5)

if current_group_left_ids > 0:
    if current_group:
        print(current_group[:-1])
