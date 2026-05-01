"""Step 4: Distribution summary — descriptive stats + univariate histograms."""
import sys
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA_PATH = sys.argv[1] if len(sys.argv) > 1 else "data/train.csv"
SKIP_COLS = {"id"}
ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)
num_cols = [c for c in df.select_dtypes(include="number").columns if c not in SKIP_COLS]
cat_cols = [c for c in df.select_dtypes(include="object").columns]

print("=" * 70)
print("DISTRIBUTION SUMMARY")
print("=" * 70)

print("\n--- NUMERIC COLUMNS ---")
desc = df[num_cols].describe(percentiles=[0.01, 0.05, 0.25, 0.5, 0.75, 0.95, 0.99]).T
desc["skew"] = df[num_cols].skew()
desc["kurtosis"] = df[num_cols].kurtosis()
with pd.option_context("display.float_format", "{:.3f}".format, "display.max_columns", 20):
    print(desc[["count", "mean", "std", "min", "1%", "5%", "25%", "50%", "75%", "95%", "99%", "max", "skew", "kurtosis"]].to_string())

print("\n--- CATEGORICAL COLUMNS ---")
for col in cat_cols:
    vc = df[col].value_counts()
    n_unique = vc.shape[0]
    print(f"\n  {col}  (n_unique={n_unique})")
    for val, cnt in vc.head(10).items():
        print(f"    {str(val):<25} {cnt:>8,}  ({cnt/len(df)*100:.1f}%)")
    if n_unique > 10:
        print(f"    ... and {n_unique - 10} more")

# Numeric histograms
ncols_plot = 3
nrows_plot = (len(num_cols) + ncols_plot - 1) // ncols_plot
fig, axes = plt.subplots(nrows_plot, ncols_plot, figsize=(15, nrows_plot * 3))
axes = axes.flatten()
for i, col in enumerate(num_cols):
    df[col].dropna().hist(ax=axes[i], bins=50, edgecolor="none", color="steelblue", alpha=0.8)
    axes[i].set_title(col, fontsize=9)
    axes[i].set_xlabel("")
for j in range(i + 1, len(axes)):
    axes[j].set_visible(False)
plt.suptitle("Univariate Distributions — Numeric Columns", fontsize=12, y=1.01)
plt.tight_layout()
plt.savefig(os.path.join(ASSETS_DIR, "distribution_histograms.png"), dpi=100, bbox_inches="tight")
plt.close()
print(f"\nHistograms saved -> {ASSETS_DIR}/distribution_histograms.png")
print("=" * 70)
