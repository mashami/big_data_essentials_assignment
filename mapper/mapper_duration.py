#!/usr/bin/env python3
import sys
from datetime import datetime

def bucket(m):
    if m <= 10:
        return "0-10min"
    elif m <= 20:
        return "10-20min"
    elif m <= 30:
        return "20-30min"
    elif m <= 60:
        return "30-60min"
    else:
        return "60+min"

for line in sys.stdin:
    fields = line.strip().split(",")
    if len(fields) != 20:
        continue
    try:
        pickup_dt = datetime.strptime(fields[1], "%Y-%m-%d %H:%M:%S")
        dropoff_dt = datetime.strptime(fields[2], "%Y-%m-%d %H:%M:%S")
        fare = float(fields[10])
        tip = float(fields[13])
        total = float(fields[16])
        distance = float(fields[4])
    except (ValueError, IndexError):
        continue
    duration_min = (dropoff_dt - pickup_dt).total_seconds() / 60.0
    print(f"{bucket(duration_min)}\t{fare},{tip},{total},{distance}")
