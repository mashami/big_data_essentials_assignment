#!/usr/bin/env python3
import sys

for line in sys.stdin:
    fields = line.strip().split(",")
    if len(fields) != 20:
        continue
    try:
        payment_type = fields[9]
        fare = float(fields[10])
        tip = float(fields[13])
        total = float(fields[16])
    except (ValueError, IndexError):
        continue
    print(f"{payment_type}\t{fare},{tip},{total}")
