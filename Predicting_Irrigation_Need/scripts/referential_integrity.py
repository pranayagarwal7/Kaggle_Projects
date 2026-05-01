"""Audit Step 3: Referential integrity — validate categorical value sets and enum membership."""
import sys
import pandas as pd

DATA_PATH = sys.argv[1] if len(sys.argv) > 1 else "data/train.csv"

ALLOWED_VALUES = {
    "Soil_Type":          {"Sandy", "Clay", "Loamy", "Silt"},
    "Crop_Type":          {"Sugarcane", "Rice", "Cotton", "Maize", "Wheat", "Potato"},
    "Crop_Growth_Stage":  {"Sowing", "Vegetative", "Flowering", "Harvest"},
    "Season":             {"Kharif", "Rabi", "Zaid"},
    "Irrigation_Type":    {"Canal", "Sprinkler", "Rainfed", "Drip"},
    "Water_Source":       {"Reservoir", "River", "Groundwater", "Rainwater"},
    "Mulching_Used":      {"Yes", "No"},
    "Region":             {"North", "South", "East", "West", "Central"},
    "Irrigation_Need":    {"Low", "Medium", "High"},
}

df = pd.read_csv(DATA_PATH)
n = len(df)

print("=" * 65)
print("REFERENTIAL INTEGRITY CHECK  (enum/value-set validation)")
print("=" * 65)
print(f"Note: Single-table dataset — no FK relationships.")
print(f"Validating categorical columns against allowed value sets.\n")

print(f"{'Column':<28} {'Allowed':>6} {'Actual':>6} {'Violations':>11}  Status")
print("-" * 65)

total_violations = 0
for col, allowed in ALLOWED_VALUES.items():
    actual_values = set(df[col].dropna().unique())
    violations = df[~df[col].isin(allowed)][col]
    viol_count = len(violations)
    unknown = actual_values - allowed
    status = "PASS" if viol_count == 0 else ("CRITICAL" if viol_count / n > 0.05 else "HIGH")
    marker = "!!" if status != "PASS" else "  "
    print(f"{marker}{col:<26} {len(allowed):>6} {len(actual_values):>6} {viol_count:>11,}  {status}")
    if unknown:
        print(f"    Unknown values: {unknown}")
    total_violations += viol_count

print()
print(f"Total violations : {total_violations:,}")
print(f"Overall status   : {'PASS' if total_violations == 0 else 'FAIL'}")
print("=" * 65)
