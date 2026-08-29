#!/usr/bin/env python3
import sys

for line in sys.stdin:
    fields = line.strip().split(",")
    if len(fields) != 20:
        continue
    pu_location = fields[7]
    print(f"{pu_location}\t1")
