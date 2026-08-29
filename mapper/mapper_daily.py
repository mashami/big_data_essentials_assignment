#!/usr/bin/env python3
import sys
from datetime import datetime

DAYS = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]

for line in sys.stdin:
    fields = line.strip().split(",")
    if len(fields) != 20:
        continue
    try:
        pickup_dt = datetime.strptime(fields[1], "%Y-%m-%d %H:%M:%S")
    except ValueError:
        continue
    print(f"{DAYS[pickup_dt.weekday()]}\t1")
