"""Audit Step 4: Business rule range validation per references/business_rule_patterns.md."""
import sys
import pandas as pd

DATA_PATH = sys.argv[1] if len(sys.argv) > 1 else "data/train.csv"

RULES = [
    # (column, min, max, description, severity_if_fail)
    ("Soil_pH",                  0.0,  14.0,  "pH scale 0–14",                        "CRITICAL"),
    ("Soil_pH",                  4.0,   9.0,  "Agronomic pH 4–9",                      "MEDIUM"),
    ("Soil_Moisture",            0.0, 100.0,  "Moisture 0–100%",                       "CRITICAL"),
    ("Organic_Carbon",           0.0,  10.0,  "OC > 0 and < 10%",                      "HIGH"),
    ("Electrical_Conductivity",  0.0,  10.0,  "EC >= 0, < 10 dS/m",                    "HIGH"),
    ("Temperature_C",          -10.0,  60.0,  "Temperature -10 to 60 C",               "HIGH"),
    ("Humidity",                 0.0, 100.0,  "Humidity 0–100%",                       "CRITICAL"),
    ("Rainfall_mm",              0.0, 5000.0, "Rainfall >= 0 and < 5000 mm/yr",        "HIGH"),
    ("Sunlight_Hours",           0.0,  24.0,  "Sunlight 0–24 hrs/day",                 "CRITICAL"),
    ("Wind_Speed_kmh",           0.0, 250.0,  "Wind >= 0 and < 250 km/h",              "HIGH"),
    ("Field_Area_hectare",       0.0, 1000.0, "Field area > 0 and < 1000 ha",          "HIGH"),
    ("Previous_Irrigation_mm",   0.0, 1000.0, "Prior irrigation >= 0 and < 1000 mm",   "MEDIUM"),
]

df = pd.read_csv(DATA_PATH)
n = len(df)

print("=" * 70)
print("VALUE RANGE VALIDATION")
print("=" * 70)
print(f"{'Column':<28} {'Rule':<30} {'Violations':>11}  {'Violation%':>10}  Severity")
print("-" * 70)

total_violations = 0
critical_count = 0
findings = []
for col, lo, hi, desc, sev in RULES:
    if col not in df.columns:
        continue
    s = df[col].dropna()
    viol = ((s < lo) | (s > hi)).sum()
    pct = viol / n * 100
    status = sev if viol > 0 else "PASS"
    marker = "!!" if status in ("CRITICAL", "HIGH") else "  "
    print(f"{marker}{col:<26} {desc:<30} {viol:>11,}  {pct:>9.3f}%  {status}")
    if viol > 0:
        total_violations += viol
        findings.append((col, desc, viol, pct, sev))
        if sev == "CRITICAL":
            critical_count += 1

print()
print(f"Total rule violations : {total_violations:,}")
print(f"CRITICAL violations   : {critical_count}")
print(f"Overall status        : {'PASS' if total_violations == 0 else 'FAIL'}")
if findings:
    print("\nFailed rules:")
    for col, desc, viol, pct, sev in findings:
        print(f"  [{sev}] {col}: {desc} -> {viol:,} rows ({pct:.3f}%)")
print("=" * 70)
