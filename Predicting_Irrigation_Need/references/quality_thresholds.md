---
name: quality_thresholds
description: Default data quality thresholds for EDA scripts
type: reference
---

# Quality Thresholds

## Null Rate
| Threshold | Status |
|-----------|--------|
| ≤ 5%      | OK     |
| 5% – 20%  | WARN   |
| > 20%     | FAIL   |

## Outlier Rate (IQR or Z-score)
| Threshold | Status |
|-----------|--------|
| ≤ 5%      | OK     |
| > 5%      | FLAG   |

## Correlation
| Threshold | Action |
|-----------|--------|
| \|r\| > 0.8 | Flag as potential multicollinearity / redundancy |

## Class Imbalance (Target)
| Threshold | Status |
|-----------|--------|
| Minority class ≥ 20% | OK |
| Minority class 10–20% | WARN |
| Minority class < 10% | FAIL |
