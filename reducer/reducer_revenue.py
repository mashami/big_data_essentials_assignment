#!/usr/bin/env python3
import sys

current_key = None
count = 0
sum_fare = sum_tip = sum_total = sum_distance = 0.0

def emit(key, n, sf, st, stot, sd):
    avg_fare = sf / n if n else 0
    avg_distance = sd / n if n else 0
    print(f"{key}\t{n}\t{sf:.2f}\t{st:.2f}\t{stot:.2f}\t{avg_fare:.2f}\t{avg_distance:.2f}")

for line in sys.stdin:
    key, value = line.strip().split("\t")
    fare, tip, total, distance = map(float, value.split(","))
    
    if key == current_key:
        count += 1
        sum_fare += fare
        sum_tip += tip
        sum_total += total
        sum_distance += distance
    else:
        if current_key is not None:
            emit(current_key, count, sum_fare, sum_tip, sum_total, sum_distance)
        current_key = key
        count = 1
        sum_fare, sum_tip, sum_total, sum_distance = fare, tip, total, distance

if current_key is not None:
    emit(current_key, count, sum_fare, sum_tip, sum_total, sum_distance)
