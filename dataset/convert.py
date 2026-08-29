import pandas as pd
import glob

for f in glob.glob("yellow_tripdata_2026-*.parquet"):
    df = pd.read_parquet(f)
    out = f.replace(".parquet", ".csv")
    df.to_csv(out, index=False)
    print(f"{f} -> {out} ({len(df):,} rows)")
