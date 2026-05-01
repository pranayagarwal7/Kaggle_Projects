# EDA Findings Summary — Predicting Irrigation Need

**Date**: 2026-04-28 | **Data**: `train.csv` (630,000 rows × 21 cols)

---

## Top Issues

### 1. TARGET IMBALANCE — "High" class = 3.3% (21,009 rows)
- Low: 58.7%, Medium: 37.9%, High: 3.3%
- A model that predicts "Low" for everything gets ~59% accuracy but zero recall on "High"
- **Action**: Use `class_weight="balanced"` or SMOTE on training fold. Evaluate with macro-F1 or per-class recall, not accuracy.

### 2. SYNTHETIC DATA — Uniform distributions, zero correlations
- All 11 numeric features have kurtosis ~-1.2 (uniform, not normal)
- All feature pairs have |r| < 0.05 — fully orthogonal
- Zero outliers across all columns
- All categoricals near-perfectly balanced
- **Implication**: Feature importances may be misleading if the DGP doesn't mirror reality. Interaction terms won't be discovered through correlation. Tree models may still work well. Don't rely on domain-intuition about feature relationships.

### 3. NO NULLS — No action needed
- All 21 columns: 0 nulls. Skip imputation step entirely.

### 4. NO OUTLIERS — No action needed
- IQR and Z-score clean on all numeric columns. No capping or Winsorization needed.

### 5. NO MULTICOLLINEARITY — All features usable
- Max |r| = 0.044. Safe to include all features without VIF filtering or PCA.

---

## Recommended Next Steps

1. **Encode categoricals**: One-hot (Soil_Type, Season, etc.) or ordinal encode (Crop_Growth_Stage: Sowing < Vegetative < Flowering < Harvest).
2. **Handle class imbalance**: Set `class_weight="balanced"` in sklearn estimators, or use stratified k-fold with SMOTE inside each fold.
3. **Baseline model**: LightGBM or XGBoost with default params — tree models handle uniform features well.
4. **Evaluation metric**: Macro-F1 or weighted-F1 given imbalance. Track per-class precision/recall for "High" specifically.
5. **Feature engineering**: With zero linear correlations, consider interaction features (e.g., `Soil_Moisture × Temperature_C`, `Rainfall_mm × Soil_Type`) — tree splits will discover non-linear combos anyway.
