import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from pathlib import Path
from datetime import datetime

DATA_DIR = Path(r"C:\Dev\investigating-orbital-sensitivity-to-inertial-variations\data")
SP3_FILE = DATA_DIR / "COD0MGXFIN_20221850000_01D_05M_ORB.SP3"

OUTPUT_DIR = DATA_DIR.parent / "results" / "experiment_008"
OUTPUT_DIR.mkdir(parents=True, exist_ok=True)

SATELLITE_ID = "R01"   # Try R01, R02, G01, E01, etc.
INERTIA_FACTORS = [0.999, 1.000, 1.001]


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

            elif line.startswith("P") and current_time is not None:
                sat = line[1:4].strip()

                records.append({
                    "time": current_time,
                    "satellite": sat,
                    "x_km": float(line[4:18]),
                    "y_km": float(line[18:32]),
                    "z_km": float(line[32:46])
                })

    return pd.DataFrame(records)


def compute_velocity(df):
    df = df.sort_values("time").copy()

    dt_seconds = df["time"].diff().dt.total_seconds()
    df["vx_km_s"] = df["x_km"].diff() / dt_seconds
    df["vy_km_s"] = df["y_km"].diff() / dt_seconds
    df["vz_km_s"] = df["z_km"].diff() / dt_seconds

    df = df.dropna().reset_index(drop=True)
    return df


def apply_inertia_variation(df, factor):
    modified = df.copy()

    # Treat inertia variation as a velocity-response perturbation.
    # Lower inertia = stronger response to velocity change.
    # Higher inertia = weaker response.
    velocity_scale = 1 / factor

    modified["mod_x_km"] = modified["x_km"].iloc[0]
    modified["mod_y_km"] = modified["y_km"].iloc[0]
    modified["mod_z_km"] = modified["z_km"].iloc[0]

    for i in range(1, len(modified)):
        dt = (modified.loc[i, "time"] - modified.loc[i - 1, "time"]).total_seconds()

        modified.loc[i, "mod_x_km"] = (
            modified.loc[i - 1, "mod_x_km"]
            + modified.loc[i, "vx_km_s"] * velocity_scale * dt
        )

        modified.loc[i, "mod_y_km"] = (
            modified.loc[i - 1, "mod_y_km"]
            + modified.loc[i, "vy_km_s"] * velocity_scale * dt
        )

        modified.loc[i, "mod_z_km"] = (
            modified.loc[i - 1, "mod_z_km"]
            + modified.loc[i, "vz_km_s"] * velocity_scale * dt
        )

    modified["real_radius_km"] = np.sqrt(
        modified["x_km"]**2 +
        modified["y_km"]**2 +
        modified["z_km"]**2
    )

    modified["modified_radius_km"] = np.sqrt(
        modified["mod_x_km"]**2 +
        modified["mod_y_km"]**2 +
        modified["mod_z_km"]**2
    )

    modified["position_error_km"] = np.sqrt(
        (modified["mod_x_km"] - modified["x_km"])**2 +
        (modified["mod_y_km"] - modified["y_km"])**2 +
        (modified["mod_z_km"] - modified["z_km"])**2
    )

    modified["radius_error_km"] = (
        modified["modified_radius_km"] - modified["real_radius_km"]
    )

    modified["inertia_factor"] = factor

    return modified


print("Loading SP3 precise orbit file...")
sp3 = parse_sp3(SP3_FILE)

print("Available satellites:")
print(sorted(sp3["satellite"].unique()))

sat_data = sp3[sp3["satellite"] == SATELLITE_ID].copy()

if sat_data.empty:
    raise ValueError(f"No data found for satellite {SATELLITE_ID}")

sat_data = compute_velocity(sat_data)

all_results = []

for factor in INERTIA_FACTORS:
    result = apply_inertia_variation(sat_data, factor)
    all_results.append(result)

results = pd.concat(all_results, ignore_index=True)

summary = results.groupby("inertia_factor").agg(
    mean_position_error_km=("position_error_km", "mean"),
    max_position_error_km=("position_error_km", "max"),
    mean_radius_error_km=("radius_error_km", "mean"),
    max_radius_error_km=("radius_error_km", "max"),
    min_radius_error_km=("radius_error_km", "min")
).reset_index()

print("\nExperiment 008 Summary")
print("----------------------")
print(f"Satellite analyzed: {SATELLITE_ID}")
print(summary)

results.to_csv(
    OUTPUT_DIR / "exp008_real_orbit_inertial_sensitivity_results.csv",
    index=False
)

summary.to_csv(
    OUTPUT_DIR / "exp008_inertial_sensitivity_summary.csv",
    index=False
)

plt.figure(figsize=(11, 6))

for factor in INERTIA_FACTORS:
    d = results[results["inertia_factor"] == factor]
    plt.plot(d["time"], d["position_error_km"], label=f"Inertia {factor}")

plt.title("Experiment 008 - Real Orbit Inertial Sensitivity")
plt.xlabel("Time UTC")
plt.ylabel("Position Error from SP3 Orbit (km)")
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "exp008_position_error_vs_time.png", dpi=300)
plt.show()

plt.figure(figsize=(11, 6))

for factor in INERTIA_FACTORS:
    d = results[results["inertia_factor"] == factor]
    plt.plot(d["time"], d["radius_error_km"], label=f"Inertia {factor}")

plt.title("Experiment 008 - Radius Error from Inertia Variation")
plt.xlabel("Time UTC")
plt.ylabel("Radius Error (km)")
plt.grid(True)
plt.legend()
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "exp008_radius_error_vs_time.png", dpi=300)
plt.show()

plt.figure(figsize=(8, 5))

plt.bar(
    summary["inertia_factor"].astype(str),
    summary["max_position_error_km"]
)

plt.title("Experiment 008 - Maximum Position Error by Inertia Factor")
plt.xlabel("Inertia Factor")
plt.ylabel("Maximum Position Error (km)")
plt.grid(axis="y")
plt.tight_layout()
plt.savefig(OUTPUT_DIR / "exp008_max_error_by_inertia_factor.png", dpi=300)
plt.show()

print("\nSaved outputs to:")
print(OUTPUT_DIR)
