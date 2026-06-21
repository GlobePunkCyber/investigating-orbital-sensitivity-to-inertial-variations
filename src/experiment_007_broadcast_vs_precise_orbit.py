import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime, timedelta

DATA_DIR = Path(r"C:\Dev\investigating-orbital-sensitivity-to-inertial-variations\data")

BRDC_FILE = DATA_DIR / "brdc1850.22g"
SP3_FILE = DATA_DIR / "COD0MGXFIN_20221850000_01D_05M_ORB.SP3"

OUTPUT_DIR = DATA_DIR.parent / "results" / "experiment_007"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)


def parse_sp3(file_path):
    records = []
    current_time = None

    with open(file_path, "r", errors="ignore") as f:
        for line in f:
            if line.startswith("*"):
                p = line.split()
                current_time = datetime(
                    int(p[1]), int(p[2]), int(p[3]),
                    int(p[4]), int(p[5]), int(float(p[6]))
                )

            elif line.startswith("PR") and current_time is not None:
                sat = line[1:4].strip()

                records.append({
                    "time": current_time,
                    "satellite": sat,
                    "sp3_x_km": float(line[4:18]),
                    "sp3_y_km": float(line[18:32]),
                    "sp3_z_km": float(line[32:46])
                })

    return pd.DataFrame(records)


def parse_glonass_brdc(file_path):
    records = []

    with open(file_path, "r", errors="ignore") as f:
        lines = f.readlines()

    start = 0
    for i, line in enumerate(lines):
        if "END OF HEADER" in line:
            start = i + 1
            break

    i = start
    while i + 3 < len(lines):
        try:
            l1, l2, l3, l4 = lines[i], lines[i+1], lines[i+2], lines[i+3]

            sat_num = int(l1[0:2])
            year = int(l1[3:5]) + 2000
            month = int(l1[6:8])
            day = int(l1[9:11])
            hour = int(l1[12:14])
            minute = int(l1[15:17])
            second = int(float(l1[18:22]))

            epoch = datetime(year, month, day, hour, minute, second)

            records.append({
                "time": epoch,
                "satellite": f"R{sat_num:02d}",
                "brdc_x_km": float(l2[4:23].replace("D", "E")),
                "brdc_y_km": float(l3[4:23].replace("D", "E")),
                "brdc_z_km": float(l4[4:23].replace("D", "E")),
            })

        except Exception:
            pass

        i += 4

    return pd.DataFrame(records)


def compare_with_time_offset(brdc, sp3, offset_hours):
    temp = brdc.copy()
    temp["time"] = temp["time"] + timedelta(hours=offset_hours)

    merged = pd.merge(temp, sp3, on=["time", "satellite"], how="inner")

    if merged.empty:
        return merged, np.inf

    merged["dx_km"] = merged["brdc_x_km"] - merged["sp3_x_km"]
    merged["dy_km"] = merged["brdc_y_km"] - merged["sp3_y_km"]
    merged["dz_km"] = merged["brdc_z_km"] - merged["sp3_z_km"]

    merged["position_error_km"] = np.sqrt(
        merged["dx_km"]**2 +
        merged["dy_km"]**2 +
        merged["dz_km"]**2
    )

    merged["brdc_radius_km"] = np.sqrt(
        merged["brdc_x_km"]**2 +
        merged["brdc_y_km"]**2 +
        merged["brdc_z_km"]**2
    )

    merged["sp3_radius_km"] = np.sqrt(
        merged["sp3_x_km"]**2 +
        merged["sp3_y_km"]**2 +
        merged["sp3_z_km"]**2
    )

    merged["radius_difference_km"] = merged["brdc_radius_km"] - merged["sp3_radius_km"]

    return merged, merged["position_error_km"].mean()


print("Loading SP3 precise orbit...")
sp3 = parse_sp3(SP3_FILE)

print("Loading GLONASS broadcast ephemeris...")
brdc = parse_glonass_brdc(BRDC_FILE)

print("SP3 records:", len(sp3))
print("Broadcast records:", len(brdc))

best_offset = None
best_error = np.inf
best_merged = None

for offset in [-3, 0, 3]:
    merged, avg_error = compare_with_time_offset(brdc, sp3, offset)
    print(f"Offset {offset:+} hours | Matches: {len(merged)} | Avg error: {avg_error:.3f} km")

    if avg_error < best_error:
        best_error = avg_error
        best_offset = offset
        best_merged = merged

merged = best_merged

if merged is None or merged.empty:
    raise ValueError("No matching records found.")

print("\nExperiment 007 Summary")
print("----------------------")
print(f"Best GLONASS time offset: {best_offset:+} hours")
print(f"Matched records: {len(merged)}")
print(f"Average position error: {merged['position_error_km'].mean():.3f} km")
print(f"Maximum position error: {merged['position_error_km'].max():.3f} km")
print(f"Minimum position error: {merged['position_error_km'].min():.3f} km")
print(f"Average radius difference: {merged['radius_difference_km'].mean():.6f} km")

summary = merged.groupby("satellite")["position_error_km"].agg(
    ["count", "mean", "max", "min"]
).reset_index()

print("\nSatellite Error Summary")
print(summary)

merged.to_csv(OUTPUT_DIR / "exp007_broadcast_vs_precise_orbit_results.csv", index=False)
summary.to_csv(OUTPUT_DIR / "exp007_satellite_error_summary.csv", index=False)

plt.figure(figsize=(11, 6))
for sat in merged["satellite"].unique():
    d = merged[merged["satellite"] == sat]
    plt.plot(d["time"], d["position_error_km"], marker="o", label=sat)

plt.title("Experiment 007 - Broadcast vs Precise Orbit Error")
plt.xlabel("Time UTC")
plt.ylabel("Position Error (km)")
plt.grid(True)
plt.legend(ncol=4, fontsize=8)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "exp007_position_error_vs_time.png", dpi=300)
plt.show()

plt.figure(figsize=(11, 6))
avg_error = summary.sort_values("mean", ascending=False)

plt.bar(avg_error["satellite"], avg_error["mean"])
plt.title("Experiment 007 - Average Position Error by Satellite")
plt.xlabel("GLONASS Satellite")
plt.ylabel("Average Position Error (km)")
plt.grid(axis="y")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "exp007_average_error_by_satellite.png", dpi=300)
plt.show()

plt.figure(figsize=(11, 6))
for sat in merged["satellite"].unique():
    d = merged[merged["satellite"] == sat]
    plt.plot(d["time"], d["radius_difference_km"], marker="o", label=sat)

plt.title("Experiment 007 - Orbital Radius Difference")
plt.xlabel("Time UTC")
plt.ylabel("Broadcast Radius - Precise Radius (km)")
plt.grid(True)
plt.legend(ncol=4, fontsize=8)
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "exp007_radius_difference.png", dpi=300)
plt.show()
