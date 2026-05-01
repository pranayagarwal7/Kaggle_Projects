# Data Quality Rubric — Predicting Irrigation Need

**Dataset**: `data/train.csv` (630,000 rows × 21 cols)
**Audit Date**: 2026-04-28

---

## Quality Dimension Scores

| Dimension | Score | Status | Key Finding |
|-----------|------:|--------|-------------|
| Completeness | 100 | PASS | 0 nulls across all 21 columns |
| Uniqueness | 100 | PASS | 0 key dups, 0 full-row dups |
| Validity | 100 | PASS | All 9 categoricals within allowed value sets |
| Accuracy | 100 | PASS | All 12 numeric range rules satisfied |
| Freshness | N/A | N/A | Static Kaggle snapshot, no SLA |
| **Overall** | **100** | **PASS** | Dataset ready for modelling |

---

## Findings

| # | Severity | Dimension | Finding | Recommended Action |
|---|----------|-----------|---------|-------------------|
| 1 | MEDIUM | Consistency | Target imbalance: High=3.3%, Medium=37.9%, Low=58.7% | `class_weight="balanced"` + macro-F1 metric |
| 2 | MEDIUM | Consistency | Synthetic data: all numeric features uniform (kurtosis~-1.2), all |r|<0.05 | Expect tree models > linear; no correlation-based feature selection |

---

## Checks Run

| Script | Result | Time |
|--------|--------|------|
| `scripts/null_counter.py` | PASS — 0/13,230,000 null cells | 2026-04-28 |
| `scripts/duplicate_finder.py` | PASS — 0 key dups, 0 full-row dups | 2026-04-28 |
| `scripts/referential_integrity.py` | PASS — 0 violations across 9 categoricals | 2026-04-28 |
| `scripts/value_range_validator.py` | PASS — 0 violations across 12 rules | 2026-04-28 |
| `scripts/freshness_check.py` | N/A — no datetime columns, static file | 2026-04-28 |

---

## Sign-off

Dataset **cleared for modelling**. Address items #1 (class imbalance) before training.
