#!/usr/bin/env python3
import random
import sys

for id_intiail in sys.stdin:
    rand_prefix = random.randint(1,9999)
    if id_intiail:
        print(str(rand_prefix).zfill(4)+'_'+id_intiail, 1, sep='\t')
