"""Audit Step 2: Full-row and key-level duplicate detection."""
import sys
import pandas as pd

DATA_PATH = sys.argv[1] if len(sys.argv) > 1 else "data/train.csv"
KEY_COL = "id"

df = pd.read_csv(DATA_PATH)
n = len(df)

# Full-row duplicates (excluding id)
feature_cols = [c for c in df.columns if c != KEY_COL]
full_row_dups = df.duplicated(subset=feature_cols, keep=False)
full_dup_count = int(full_row_dups.sum())

# Key-level duplicates
key_dups = df.duplicated(subset=[KEY_COL], keep=False)
key_dup_count = int(key_dups.sum())

print("=" * 65)
print("DUPLICATE DETECTION")
print("=" * 65)
print(f"Total rows       : {n:,}")
print()
print(f"--- KEY DUPLICATES (on '{KEY_COL}') ---")
print(f"  Duplicate rows : {key_dup_count:,}  ({key_dup_count/n*100:.3f}%)")
if key_dup_count > 0:
    print(f"  Severity       : CRITICAL")
    dup_sample = df[key_dups][[KEY_COL]].value_counts().head(10)
    print("  Top duplicate keys:")
    for k, cnt in dup_sample.items():
        print(f"    {k}: {cnt} occurrences")
else:
    print(f"  Severity       : PASS")

print()
print(f"--- FULL-ROW DUPLICATES (excluding '{KEY_COL}') ---")
print(f"  Duplicate rows : {full_dup_count:,}  ({full_dup_count/n*100:.3f}%)")
if full_dup_count > 0:
    severity = "HIGH" if full_dup_count / n > 0.01 else "MEDIUM"
    print(f"  Severity       : {severity}")
    print("  Sample duplicate rows:")
    print(df[full_row_dups][feature_cols].drop_duplicates().head(3).to_string(index=False))
else:
    print(f"  Severity       : PASS")

print()
print("SUMMARY")
print(f"  Key duplicates  : {'CRITICAL' if key_dup_count > 0 else 'PASS'}")
print(f"  Full-row dups   : {'FAIL' if full_dup_count > 0 else 'PASS'}  ({full_dup_count:,} rows)")
print("=" * 65)
