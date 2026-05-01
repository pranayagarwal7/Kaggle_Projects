"""Step 5: Correlation exploration — Pearson heatmap, flag |r| > 0.8 pairs."""
import sys
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import seaborn as sns

DATA_PATH = sys.argv[1] if len(sys.argv) > 1 else "data/train.csv"
SKIP_COLS = {"id"}
HIGH_CORR_THRESH = 0.8
ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)
num_cols = [c for c in df.select_dtypes(include="number").columns if c not in SKIP_COLS]

corr = df[num_cols].corr()

print("=" * 65)
print("CORRELATION EXPLORER")
print("=" * 65)
print(f"\nCorrelation matrix ({len(num_cols)} numeric features):")
with pd.option_context("display.float_format", "{:.3f}".format):
    print(corr.to_string())

print(f"\n--- HIGH CORRELATION PAIRS (|r| > {HIGH_CORR_THRESH}) ---")
high_pairs = []
for i in range(len(corr.columns)):
    for j in range(i + 1, len(corr.columns)):
        r = corr.iloc[i, j]
        if abs(r) > HIGH_CORR_THRESH:
            high_pairs.append((corr.columns[i], corr.columns[j], r))

if high_pairs:
    for col_a, col_b, r in sorted(high_pairs, key=lambda x: abs(x[2]), reverse=True):
        print(f"  {col_a:<28} <-> {col_b:<28}  r={r:+.3f}")
else:
    print("  None found — no multicollinearity risk above threshold.")

# Heatmap
fig, ax = plt.subplots(figsize=(12, 10))
mask = np.triu(np.ones_like(corr, dtype=bool))
sns.heatmap(corr, mask=mask, annot=True, fmt=".2f", cmap="coolwarm",
            center=0, vmin=-1, vmax=1, linewidths=0.5, ax=ax,
            annot_kws={"size": 8})
ax.set_title("Pearson Correlation Matrix (lower triangle)", fontsize=12)
plt.tight_layout()
plt.savefig(os.path.join(ASSETS_DIR, "correlation_heatmap.png"), dpi=100, bbox_inches="tight")
plt.close()
print(f"\nHeatmap saved -> {ASSETS_DIR}/correlation_heatmap.png")
print("=" * 65)
