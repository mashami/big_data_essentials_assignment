#!/usr/bin/env python3
"""
Minimal Hadoop Mapper - Count trips by pickup hour
"""
import sys
from datetime import datetime

HEADER = "VendorID"
FIELD_COUNT = 20
HOUR_INDEX = 1

for line in sys.stdin:
    line = line.strip()
    if not line or line.startswith(HEADER):
        continue
    
    fields = line.split(",")
    if len(fields) != FIELD_COUNT:
        continue
    
    try:
        pickup_hour = datetime.strptime(
            fields[HOUR_INDEX], 
            "%Y-%m-%d %H:%M:%S"
        ).hour
        print(f"{pickup_hour:02d}\t1")
    except ValueError:
        continue
