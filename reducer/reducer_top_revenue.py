#!/usr/bin/env python3
import sys

records = []

for line in sys.stdin:
    line = line.rstrip("\n")
    try:
        key, row = line.split("\t", 1)
    except ValueError:
        continue
    
    fields = row.split("\t")
    try:
        revenue = float(fields[4])
    except (IndexError, ValueError):
        continue
    
    records.append((revenue, row))

records.sort(key=lambda x: x[0], reverse=True)

for revenue, row in records[:10]:
    print(row)
