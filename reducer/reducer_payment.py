#!/usr/bin/env python3
import sys

current_key = None
count = 0
sum_fare = sum_tip = sum_total = 0.0

def emit(key, n, sf, st, stot):
    avg_fare = sf / n if n else 0
    avg_tip = st / n if n else 0
    print(f"{key}\t{n}\t{stot:.2f}\t{avg_fare:.2f}\t{avg_tip:.2f}")

for line in sys.stdin:
    key, value = line.strip().split("\t")
    fare, tip, total = map(float, value.split(","))
    
    if key == current_key:
        count += 1
        sum_fare += fare
        sum_tip += tip
        sum_total += total
    else:
        if current_key is not None:
            emit(current_key, count, sum_fare, sum_tip, sum_total)
        current_key = key
        count = 1
        sum_fare, sum_tip, sum_total = fare, tip, total

if current_key is not None:
    emit(current_key, count, sum_fare, sum_tip, sum_total)
