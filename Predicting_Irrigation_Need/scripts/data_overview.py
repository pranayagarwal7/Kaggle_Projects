"""Step 1: Load and overview — row count, dtypes, memory, sample, grain confirmation."""
import sys
import pandas as pd

DATA_PATH = sys.argv[1] if len(sys.argv) > 1 else "data/train.csv"
TARGET = "Irrigation_Need"
ID_COL = "id"

df = pd.read_csv(DATA_PATH)

print("=" * 60)
print("DATA OVERVIEW")
print("=" * 60)
print(f"Rows         : {len(df):,}")
print(f"Columns      : {df.shape[1]}")
print(f"Memory usage : {df.memory_usage(deep=True).sum() / 1e6:.2f} MB")
print()

print("--- DTYPES ---")
dtype_counts = df.dtypes.value_counts()
for dtype, count in dtype_counts.items():
    print(f"  {str(dtype):<15} {count} column(s)")
print()

print("--- COLUMN TYPES ---")
num_cols = df.select_dtypes(include="number").columns.tolist()
cat_cols = df.select_dtypes(include="object").columns.tolist()
print(f"  Numeric ({len(num_cols)}): {num_cols}")
print(f"  Categorical ({len(cat_cols)}): {cat_cols}")
print()

print("--- TARGET DISTRIBUTION ---")
if TARGET in df.columns:
    vc = df[TARGET].value_counts()
    for val, cnt in vc.items():
        print(f"  {val:<12} {cnt:>8,}  ({cnt/len(df)*100:.1f}%)")
print()

print("--- SAMPLE (5 rows) ---")
print(df.sample(5, random_state=42).to_string(index=False))
print()

print("--- GRAIN ---")
id_unique = df[ID_COL].nunique() if ID_COL in df.columns else None
print(f"  id unique values : {id_unique:,}" if id_unique else "  No id column found")
print(f"  Grain: one row = one field observation with crop/soil/weather context")
print("=" * 60)
