"""Audit Step 1: Column-by-column null profile with business-context thresholds."""
import sys
import pandas as pd

DATA_PATH = sys.argv[1] if len(sys.argv) > 1 else "data/train.csv"
CRITICAL_THRESHOLD = 0.20
HIGH_THRESHOLD = 0.05
MEDIUM_THRESHOLD = 0.01

df = pd.read_csv(DATA_PATH)
n = len(df)

null_counts = df.isnull().sum()
null_rates = null_counts / n

results = []
for col in df.columns:
    rate = null_rates[col]
    count = int(null_counts[col])
    if rate > CRITICAL_THRESHOLD:
        severity = "CRITICAL"
    elif rate > HIGH_THRESHOLD:
        severity = "HIGH"
    elif rate > MEDIUM_THRESHOLD:
        severity = "MEDIUM"
    elif rate > 0:
        severity = "LOW"
    else:
        severity = "PASS"
    results.append({"column": col, "null_count": count, "null_rate": rate, "severity": severity})

df_results = pd.DataFrame(results)
failures = df_results[df_results["severity"] != "PASS"]

print("=" * 65)
print("NULL & COMPLETENESS AUDIT")
print("=" * 65)
print(f"Rows: {n:,}  |  Columns: {df.shape[1]}")
print(f"Thresholds: CRITICAL>{CRITICAL_THRESHOLD*100:.0f}%  HIGH>{HIGH_THRESHOLD*100:.0f}%  MEDIUM>{MEDIUM_THRESHOLD*100:.0f}%")
print()
print(f"{'Column':<30} {'Null Count':>11} {'Null Rate':>10}  Severity")
print("-" * 65)
for _, row in df_results.iterrows():
    marker = "!!" if row["severity"] in ("CRITICAL", "HIGH") else "  "
    print(f"{marker}{row['column']:<28} {row['null_count']:>11,} {row['null_rate']*100:>9.3f}%  {row['severity']}")

print()
print(f"PASS : {(df_results['severity']=='PASS').sum()}/{len(df_results)} columns")
print(f"FAIL : {len(failures)} columns  {list(failures['column']) if len(failures) else '(none)'}")
total = null_counts.sum()
print(f"Total null cells: {total:,}  ({total/(n*df.shape[1])*100:.4f}% of dataset)")
print("=" * 65)
