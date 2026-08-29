#!/usr/bin/env python3
import sys

for line in sys.stdin:
    fields = line.strip().split(",")
    if len(fields) != 20:
        continue
    try:
        pu = fields[7]
        fare = float(fields[10])
        tip = float(fields[13])
        total = float(fields[16])
        distance = float(fields[4])
    except (ValueError, IndexError):
        continue
    print(f"{pu}\t{fare},{tip},{total},{distance}")
