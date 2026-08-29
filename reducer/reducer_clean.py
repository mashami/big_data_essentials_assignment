#!/usr/bin/env python3
import sys

current_key = None
first_occurrence = True

for line in sys.stdin:
    line = line.rstrip("\n")
    try:
        key, row = line.split("\t", 1)
    except ValueError:
        continue
    
    if key != current_key:
        if not first_occurrence:
            print(row)
        else:
            print(row)
            first_occurrence = False
        current_key = key
    else:
        sys.stderr.write("reporter:counter:Anomalies,DuplicateRecord,1\n")
