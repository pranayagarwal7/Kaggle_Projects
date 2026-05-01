"""Step 2: Null profile — per-column null counts and rates, flagged against thresholds."""
import sys
import pandas as pd

DATA_PATH = sys.argv[1] if len(sys.argv) > 1 else "data/train.csv"
WARN_THRESHOLD = 0.05   # 5%
FAIL_THRESHOLD = 0.20   # 20%

df = pd.read_csv(DATA_PATH)
n = len(df)

null_counts = df.isnull().sum()
null_rates = null_counts / n

report = pd.DataFrame({
    "null_count": null_counts,
    "null_rate": null_rates,
}).sort_values("null_rate", ascending=False)

report["status"] = "OK"
report.loc[report["null_rate"] > WARN_THRESHOLD, "status"] = "WARN"
report.loc[report["null_rate"] > FAIL_THRESHOLD, "status"] = "FAIL"

print("=" * 60)
print("NULL PROFILE")
print("=" * 60)
print(f"Thresholds: WARN > {WARN_THRESHOLD*100:.0f}%  |  FAIL > {FAIL_THRESHOLD*100:.0f}%")
print()
print(f"{'Column':<30} {'Nulls':>8} {'Rate':>8}  Status")
print("-" * 60)
for col, row in report.iterrows():
    flag = "**" if row["status"] != "OK" else "  "
    print(f"{flag}{col:<28} {int(row['null_count']):>8,} {row['null_rate']*100:>7.2f}%  {row['status']}")

print()
total_nulls = null_counts.sum()
print(f"Total null cells : {total_nulls:,} / {n * df.shape[1]:,}  ({total_nulls / (n * df.shape[1]) * 100:.3f}%)")
warn_cols = report[report["status"] == "WARN"]["null_rate"].index.tolist()
fail_cols = report[report["status"] == "FAIL"]["null_rate"].index.tolist()
print(f"WARN columns     : {warn_cols if warn_cols else 'None'}")
print(f"FAIL columns     : {fail_cols if fail_cols else 'None'}")
print("=" * 60)
