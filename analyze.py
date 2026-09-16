# analyze.py
# Breakdown-risk analysis for Vossberg Mobility fleet.
#
# Key finding: load_factor (how hard a car is driven relative to its capacity) and
# km_since_service (time overdue for a service) are the strongest predictors of breakdown.
# Total odometer mileage and age look obvious but barely separate the two groups in this
# dataset — high-mileage, old cars are no more likely to have broken down than low-mileage ones.

import pandas as pd

df = pd.read_csv("fleet_history.csv", encoding="latin-1")

# ── 1. Compare group means for every numeric feature ─────────────────────────
print("=== Mean values: broken-down cars vs intact cars ===")
numeric_cols = ["odometer_km", "km_since_service", "avg_daily_km", "load_factor", "age_years"]
group_means = df.groupby("broke_down")[numeric_cols].mean()
print(group_means.to_string())
print()

# ── 2. Compute per-feature separation ratio (broken mean / intact mean) ──────
intact = df[df["broke_down"] == 0]
broken = df[df["broke_down"] == 1]

print("=== Separation ratio (broken mean / intact mean) — higher = stronger signal ===")
ratios = {}
for col in numeric_cols:
    intact_mean = intact[col].mean()
    broken_mean = broken[col].mean()
    ratio = broken_mean / intact_mean if intact_mean != 0 else float("inf")
    ratios[col] = ratio
    print(f"  {col:<22} intact={intact_mean:.2f}  broken={broken_mean:.2f}  ratio={ratio:.3f}")
print()

# ── 3. Build a 0–100 risk score from the two strongest features ──────────────
# load_factor and km_since_service have the highest separation ratios.
# Normalise each 0–1 across the full fleet, average them, scale to 100.

def normalise(series: pd.Series) -> pd.Series:
    lo, hi = series.min(), series.max()
    if hi == lo:
        return pd.Series([0.0] * len(series), index=series.index)
    return (series - lo) / (hi - lo)

df["risk_score"] = (
    normalise(df["load_factor"]) * 0.55
    + normalise(df["km_since_service"]) * 0.45
) * 100

# ── 4. Print cars ranked by risk, highest first ──────────────────────────────
ranked = df[["car_id", "load_factor", "km_since_service", "risk_score", "broke_down"]].sort_values(
    "risk_score", ascending=False
)

print("=== Fleet ranked by breakdown risk (highest first) ===")
print(f"{'car_id':<12} {'load_factor':>12} {'km_since_svc':>13} {'risk_score':>11} {'broke_down':>11}")
print("-" * 65)
for _, row in ranked.iterrows():
    flag = " * broke" if row["broke_down"] == 1 else ""
    print(
        f"{row['car_id']:<12} {row['load_factor']:>12.2f} {row['km_since_service']:>13.0f}"
        f" {row['risk_score']:>11.1f}{flag}"
    )

print()
print(f"Total cars: {len(df)}   Breakdowns: {df['broke_down'].sum()}   "
      f"Breakdown rate: {df['broke_down'].mean()*100:.1f}%")
print()
print("Top-10 risk cars that had NOT yet hit the 80% service threshold:")
threshold_km = 15000 * 0.80   # 12,000 km
pre_flag = ranked[(ranked["km_since_service"] < threshold_km)].head(10)
print(pre_flag[["car_id", "load_factor", "km_since_service", "risk_score", "broke_down"]].to_string(index=False))
