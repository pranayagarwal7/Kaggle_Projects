# EDA Report — Predicting Irrigation Need

**Dataset**: `data/train.csv`
**Date**: 2026-04-28
**Analyst**: Pranay Agarwal

---

## 1. Dataset Overview

| Property | Value |
|----------|-------|
| Rows | 630,000 |
| Columns | 21 |
| Memory usage | 369.48 MB |
| Numeric columns | 11 (float64 × 11, int64 × 1 = id) |
| Categorical columns | 9 |
| Null cells | 0 (0.000%) |

**Grain**: One row = one agricultural field observation with soil, crop, weather, and management context. `id` is unique per row (630,000 distinct values — confirmed no duplicates).

---

## 2. Target Distribution

| Class | Count | Share |
|-------|------:|------:|
| Low | 369,917 | 58.7% |
| Medium | 239,074 | 37.9% |
| High | 21,009 | 3.3% |

**Note**: Moderate imbalance. "High" class is severely under-represented (3.3%). Recommend class-weighted loss or SMOTE before modelling.

---

## 3. Null Profile

**Result: PASS** — Zero nulls across all 21 columns. No imputation required.

---

## 4. Outlier Detection (IQR + Z-score, threshold >5%)

**Result: PASS** — Zero IQR or Z-score outliers on all 11 numeric columns.

| Column | IQR Outliers | IQR % | Z Outliers | Z % |
|--------|------------:|------:|-----------:|----:|
| Soil_pH | 0 | 0.00% | 0 | 0.00% |
| Soil_Moisture | 0 | 0.00% | 0 | 0.00% |
| Organic_Carbon | 0 | 0.00% | 0 | 0.00% |
| Electrical_Conductivity | 0 | 0.00% | 0 | 0.00% |
| Temperature_C | 0 | 0.00% | 0 | 0.00% |
| Humidity | 0 | 0.00% | 0 | 0.00% |
| Rainfall_mm | 0 | 0.00% | 0 | 0.00% |
| Sunlight_Hours | 0 | 0.00% | 0 | 0.00% |
| Wind_Speed_kmh | 0 | 0.00% | 0 | 0.00% |
| Field_Area_hectare | 0 | 0.00% | 0 | 0.00% |
| Previous_Irrigation_mm | 0 | 0.00% | 0 | 0.00% |

**Boxplot**: `assets/outlier_boxplots.png`

---

## 5. Distribution Summary

### Numeric Columns

| Column | Mean | Std | Min | Max | Skew | Kurtosis |
|--------|-----:|----:|----:|----:|-----:|---------:|
| Soil_pH | 6.48 | 0.92 | 4.80 | 8.20 | 0.07 | -1.15 |
| Soil_Moisture | 37.30 | 16.38 | 8.00 | 65.00 | -0.06 | -1.18 |
| Organic_Carbon | 0.92 | 0.37 | 0.30 | 1.60 | 0.11 | -1.17 |
| Electrical_Conductivity | 1.75 | 0.95 | 0.10 | 3.50 | 0.05 | -1.15 |
| Temperature_C | 27.00 | 8.62 | 12.00 | 42.00 | 0.00 | -1.21 |
| Humidity | 61.56 | 19.71 | 25.00 | 95.00 | -0.09 | -1.16 |
| Rainfall_mm | 1462.21 | 612.99 | 0.38 | 2499.69 | -0.12 | -0.94 |
| Sunlight_Hours | 7.51 | 2.00 | 4.00 | 11.00 | -0.04 | -1.21 |
| Wind_Speed_kmh | 10.38 | 5.69 | 0.50 | 20.00 | -0.03 | -1.24 |
| Field_Area_hectare | 7.52 | 4.22 | 0.30 | 15.00 | 0.05 | -1.18 |
| Previous_Irrigation_mm | 62.32 | 34.25 | 0.02 | 119.99 | -0.02 | -1.26 |

**Pattern**: All numeric features show near-zero skew (<0.15) and kurtosis ~-1.2 (strongly platykurtic = uniform-like). This is consistent with synthetic data generation.

**Histograms**: `assets/distribution_histograms.png`

### Categorical Columns

| Column | n_unique | Distribution |
|--------|:--------:|-------------|
| Soil_Type | 4 | Sandy 26.4%, Clay 25.2%, Loamy 24.8%, Silt 23.6% |
| Crop_Type | 6 | Near-equal ~16–17% each |
| Crop_Growth_Stage | 4 | Near-equal ~23–27% each |
| Season | 3 | Kharif 34.4%, Rabi 33.0%, Zaid 32.6% |
| Irrigation_Type | 4 | Near-equal ~24–26% each |
| Water_Source | 4 | Near-equal ~24–26% each |
| Region | 5 | Near-equal ~18–21% each |
| Mulching_Used | 2 | No 50.2%, Yes 49.8% |

All categoricals are near-perfectly balanced — further evidence of synthetic dataset.

---

## 6. Correlation Exploration

**Result: PASS** — No feature pairs with |r| > 0.8. Max absolute correlation observed: ~0.044 (Rainfall_mm vs Soil_Moisture).

All 55 feature pairs have |r| < 0.05. Features are essentially orthogonal — no multicollinearity risk.

**Heatmap**: `assets/correlation_heatmap.png`

---

## 7. EDA Checklist Sign-off

| Item | Status |
|------|--------|
| Row count and grain confirmed | PASS |
| Duplicate rows checked (id unique) | PASS |
| Null profile complete | PASS (0 nulls) |
| Outlier detection complete | PASS (0 flagged) |
| Target distribution reviewed | NOTE: High class = 3.3% imbalance |
| Numeric distributions reviewed | PASS (uniform-like, synthetic) |
| Categorical distributions reviewed | PASS (balanced) |
| Correlation matrix reviewed | PASS (no multicollinearity) |
| Data quality risk documented | PASS |

**Dataset declared profiled.**
