# Quality Dimensions Reference

## Dimension Definitions

| Dimension | Definition | Script | Severity Scale |
|-----------|------------|--------|----------------|
| **Completeness** | No missing values in required fields | `null_counter.py` | CRITICAL >20% / HIGH >5% / MEDIUM >1% |
| **Uniqueness** | No unintended duplicate records | `duplicate_finder.py` | CRITICAL if key dups exist / HIGH if >1% full-row dups |
| **Validity** | Values conform to allowed sets and formats | `referential_integrity.py` | CRITICAL if >5% violations / HIGH if any violations |
| **Accuracy** | Values within expected business-rule ranges | `value_range_validator.py` | Per rule — see business_rule_patterns.md |
| **Freshness** | Data is up to date per pipeline SLA | `freshness_check.py` | CRITICAL >30 days / HIGH >7 days |
| **Consistency** | Cross-column logical rules hold | manual / future script | Case-by-case |

## Severity Levels

| Severity | Meaning | Action |
|----------|---------|--------|
| CRITICAL | Data unusable — blocks downstream use | Stop pipeline, page on-call |
| HIGH | Significant quality issue — investigate before use | File ticket, notify consumers |
| MEDIUM | Minor issue — monitor trend | Log and review at next QA cycle |
| LOW | Informational — no immediate action | Record in audit log |
| PASS | Dimension fully passes | No action |
| N/A | Check not applicable (e.g. freshness on static file) | Document reason |

## Scoring Model

Each dimension scores 0–100:
- PASS = 100
- LOW finding = 90
- MEDIUM finding = 70
- HIGH finding = 40
- CRITICAL finding = 0

Overall dataset score = mean of all applicable dimension scores.
