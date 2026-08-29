import pandas as pd
import time
import glob
import psutil
import os

process = psutil.Process(os.getpid())
mem_before = process.memory_info().rss / 1e6

start = time.time()

cols = ["PULocationID", "fare_amount", "tip_amount", "total_amount", "trip_distance"]
dfs = []
for f in glob.glob("yellow_tripdata_2026-*.csv"):
    df = pd.read_csv(f, usecols=cols)
    dfs.append(df)

full = pd.concat(dfs, ignore_index=True)

result = full.groupby("PULocationID").agg(
    trip_count=("fare_amount", "count"),
    total_fare=("fare_amount", "sum"),
    total_tip=("tip_amount", "sum"),
    total_revenue=("total_amount", "sum"),
    avg_fare=("fare_amount", "mean"),
    avg_distance=("trip_distance", "mean"),
)

elapsed = time.time() - start
mem_after = process.memory_info().rss / 1e6

print(f"Rows processed: {len(full):,}")
print(f"Zones: {len(result)}")
print(f"Execution time: {elapsed:.2f} seconds")
print(f"Memory used: {mem_after - mem_before:.1f} MB (delta), {mem_after:.1f} MB (peak RSS)")
