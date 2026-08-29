#!/usr/bin/env python3
import sys

for line in sys.stdin:
    line = line.strip()
    fields = line.split(",")
    if len(fields) != 20:
        continue
    try:
        distance = float(fields[4])
        fare = float(fields[10])
        total = float(fields[16])
    except (ValueError, IndexError):
        continue
    if distance <= 0:
        continue
    fare_per_mile = fare / distance
    reasons = []
    if fare_per_mile > 50:
        reasons.append("ExtremeFarePerMile_High")
    if fare_per_mile < 1:
        reasons.append("ExtremeFarePerMile_Low")
    if total > 300:
        reasons.append("ExtremeTotalAmount")
    if reasons:
        print(f"{'|'.join(reasons)}\t{line}")
