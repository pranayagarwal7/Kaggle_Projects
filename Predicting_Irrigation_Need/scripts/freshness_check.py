"""Audit Step 5: Freshness check — timestamp column detection and staleness assessment."""
import sys
import os
import pandas as pd
from datetime import datetime

DATA_PATH = sys.argv[1] if len(sys.argv) > 1 else "data/train.csv"

df = pd.read_csv(DATA_PATH)

# Detect datetime columns
datetime_cols = []
for col in df.columns:
    if df[col].dtype == "object":
        sample = df[col].dropna().head(100)
        try:
            pd.to_datetime(sample, infer_datetime_format=True)
            datetime_cols.append(col)
        except Exception:
            pass

# File modification time as proxy
file_mtime = os.path.getmtime(DATA_PATH)
file_mod_dt = datetime.fromtimestamp(file_mtime)
now = datetime.now()
file_age_days = (now - file_mod_dt).days

print("=" * 65)
print("FRESHNESS CHECK")
print("=" * 65)
print(f"File path        : {DATA_PATH}")
print(f"File last modified: {file_mod_dt.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"Current date      : {now.strftime('%Y-%m-%d %H:%M:%S')}")
print(f"File age          : {file_age_days} day(s)")
print()

if datetime_cols:
    print(f"Detected datetime columns: {datetime_cols}")
    for col in datetime_cols:
        parsed = pd.to_datetime(df[col], infer_datetime_format=True, errors="coerce")
        latest = parsed.max()
        oldest = parsed.min()
        lag_days = (now - latest).days
        print(f"\n  Column: {col}")
        print(f"    Oldest record  : {oldest}")
        print(f"    Newest record  : {latest}")
        print(f"    Lag from now   : {lag_days} days")
        status = "PASS" if lag_days <= 7 else ("HIGH" if lag_days <= 30 else "CRITICAL")
        print(f"    Status         : {status}")
else:
    print("No datetime columns found.")
    print("Dataset type: Static Kaggle competition file — no freshness SLA applies.")
    print("Status: N/A (static snapshot)")

print()
print(f"Overall freshness status: {'N/A — static file' if not datetime_cols else 'see above'}")
print("=" * 65)
