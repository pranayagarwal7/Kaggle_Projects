"""Step 3: Outlier detection — IQR + z-score on numeric columns. Saves plot to assets/."""
import sys
import os
import pandas as pd
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

DATA_PATH = sys.argv[1] if len(sys.argv) > 1 else "data/train.csv"
SKIP_COLS = {"id"}
Z_THRESH = 3.0
ASSETS_DIR = "assets"
os.makedirs(ASSETS_DIR, exist_ok=True)

df = pd.read_csv(DATA_PATH)
num_cols = [c for c in df.select_dtypes(include="number").columns if c not in SKIP_COLS]

print("=" * 65)
print("OUTLIER DETECTION  (IQR + Z-score)")
print("=" * 65)
print(f"{'Column':<30} {'IQR_outliers':>13} {'IQR_%':>7}  {'Z_outliers':>12} {'Z_%':>6}")
print("-" * 65)

summary = []
for col in num_cols:
    s = df[col].dropna()
    q1, q3 = s.quantile(0.25), s.quantile(0.75)
    iqr = q3 - q1
    lower, upper = q1 - 1.5 * iqr, q3 + 1.5 * iqr
    iqr_out = int(((s < lower) | (s > upper)).sum())
    iqr_pct = iqr_out / len(s) * 100

    z = np.abs((s - s.mean()) / s.std())
    z_out = int((z > Z_THRESH).sum())
    z_pct = z_out / len(s) * 100

    flag = " **" if iqr_pct > 5 or z_pct > 5 else "   "
    print(f"{flag}{col:<27} {iqr_out:>13,} {iqr_pct:>6.2f}%  {z_out:>12,} {z_pct:>5.2f}%")
    summary.append({"col": col, "iqr_outliers": iqr_out, "iqr_pct": iqr_pct,
                    "z_outliers": z_out, "z_pct": z_pct,
                    "min": s.min(), "max": s.max(), "mean": s.mean(), "median": s.median()})

print()
flagged = [r["col"] for r in summary if r["iqr_pct"] > 5 or r["z_pct"] > 5]
print(f"Flagged columns (>5% outliers): {flagged if flagged else 'None'}")

# Boxplot grid
ncols_plot = 3
nrows_plot = (len(num_cols) + ncols_plot - 1) // ncols_plot
fig, axes = plt.subplots(nrows_plot, ncols_plot, figsize=(15, nrows_plot * 3))
axes = axes.flatten()
for i, col in enumerate(num_cols):
    df[col].dropna().plot.box(ax=axes[i], vert=True)
    axes[i].set_title(col, fontsize=9)
for j in range(i + 1, len(axes)):
    axes[j].set_visible(False)
plt.suptitle("Boxplots — Outlier Overview", fontsize=12, y=1.01)
plt.tight_layout()
plt.savefig(os.path.join(ASSETS_DIR, "outlier_boxplots.png"), dpi=100, bbox_inches="tight")
plt.close()
print(f"\nBoxplot saved -> {ASSETS_DIR}/outlier_boxplots.png")
print("=" * 65)
