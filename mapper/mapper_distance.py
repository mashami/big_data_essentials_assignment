#!/usr/bin/env python3
import sys

def bucket(d):
    if d <= 2:
        return "0-2"
    elif d <= 5:
        return "2-5"
    elif d <= 10:
        return "5-10"
    elif d <= 20:
        return "10-20"
    else:
        return "20+"

for line in sys.stdin:
    fields = line.strip().split(",")
    if len(fields) != 20:
        continue
    try:
        fare = float(fields[10])
        tip = float(fields[13])
        total = float(fields[16])
        distance = float(fields[4])
    except (ValueError, IndexError):
        continue
    print(f"{bucket(distance)}\t{fare},{tip},{total},{distance}")
